# Integrating umtoken into a model

umtoken does not return a scalar token id but a tuple — `(vocab_id, prop_id)`,
or `(vocab_id, rule_id, ws_id + 2 * up_id)` if you want the model to generalize
over rule and case combinations it has not seen. A transformer therefore needs
adapting in two places:

* **the input side**, which is easy: embed each component and add.
* **the output side**, which is the interesting part: the components of one
  token are not independent, so predicting them with independent heads loses
  accuracy.

If you only want to tokenize text, you need none of this — see the quick start
in the [README](../README.md#quick-start).

## Input side

```python
self.emb_0 = nn.Embedding(vocab_size, d_model)   # vocabulary ids
self.emb_1 = nn.Embedding(props_size, d_model)   # property ids

def embed(self, input_ids):          # (batch, seq, 2)
    return self.emb_0(input_ids[..., 0]) + self.emb_1(input_ids[..., 1])
```

If your ids arrive packed as scalars — which is what the Hugging Face wrapper
does by default — unpack them first:

```python
input_ids_0 = input_ids % vocab_size
input_ids_1 = input_ids // vocab_size
```

## Output side: a recursive head

The naive approach is one linear projection per component. It is wrong in a
specific way: the property is highly predictable *given* the vocabulary entry
and nearly unpredictable without it. Independent heads cannot use that.

The head below predicts the components **autoregressively within a token**.
Head 0 projects the transformer output to the vocabulary. Every later head first
merges the running state with the embedding of the component before it, through
a GLU, and only then projects. During training the fed-back embeddings come from
the labels (teacher forcing); at inference they come from the ids just chosen.

This generalizes to any number of components, so it serves 2-tuples and
3-tuples alike — `d_heads=[vocab_size, props_size]` or
`d_heads=[vocab_size, rules_size, ws_case_size]`.

```python
from typing import List, Literal, Optional, Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F


class MultiValuedRecursiveHead(nn.Module):
    """Output head for tokens that are tuples of ids instead of a single id.

    One head per component of the tuple. Head 0 predicts the first component
    from the transformer output alone; every later head additionally sees the
    embedding of the component before it, so the components are predicted
    autoregressively *within* a token.

    Args:
        d_model: width of the transformer output.
        d_heads: vocabulary size of each component, e.g. [vocab_size, props_size].
        emb_norm: normalize the fed-back embeddings.
        infer_max_k: default per-head beam cap for infer() (0 = no cap).
        infer_search_mode: default search mode for infer().
        loss_weights: per-head weight in the summed loss (training).
        loss_weights_eval: per-head weight in the summed loss (eval).
    """

    def __init__(self,
                 d_model: int,
                 d_heads: List[int],
                 emb_norm: bool = True,
                 infer_max_k: Optional[List[int]] = None,
                 infer_search_mode: Optional[Literal["beam", "sample", "greedy"]] = None,
                 loss_weights: Optional[Tuple[float]] = None,
                 loss_weights_eval: Optional[Tuple[float]] = None):
        super().__init__()
        self.d_model = d_model
        self.d_heads = d_heads
        self.emb_norm = emb_norm
        self.infer_max_k = infer_max_k
        self.infer_search_mode = infer_search_mode
        self.loss_weights = loss_weights
        self.loss_weights_eval = loss_weights_eval
        self.n_heads = len(d_heads)

        assert loss_weights is None or len(loss_weights) == self.n_heads, "loss_weights length must match number of heads"
        assert loss_weights_eval is None or len(loss_weights_eval) == self.n_heads, "loss_weights_eval length must match number of heads"
        assert infer_max_k is None or len(infer_max_k) == self.n_heads, "infer_max_k length must match number of heads"
        assert infer_search_mode is None or infer_search_mode in ["beam", "sample", "greedy"], "infer_search_mode must be 'beam', 'sample' or 'greedy'"

        self.nrm_inp = nn.RMSNorm(d_model)
        self.nrm_emb = nn.RMSNorm(d_model)
        # the recursive step: a GLU merging the running state with the previous
        # component's embedding
        self.linear_in = nn.ModuleList([nn.Linear(2 * d_model, d_model) for _ in range(self.n_heads - 1)])
        self.linear_gate = nn.ModuleList([nn.Linear(2 * d_model, d_model) for _ in range(self.n_heads - 1)])
        self.linear_out = nn.ModuleList([nn.Linear(d_model, d_head) for d_head in d_heads])

    def forward(self, x: torch.Tensor, emb: torch.Tensor, lbl: Optional[torch.Tensor] = None,
                return_logits: bool = True, return_loss: bool = False,
                return_errors: bool = False, return_error_rate: bool = False) -> dict:
        """
        Args:
            x: transformer output, shape (*, d_model).
            emb: embeddings of the true components, shape (*, N-1, d_model).
                 During training these come from the labels (teacher forcing).
            lbl: labels, shape (*, N). Required for loss/errors. -100 is ignored.
            return_logits: return per-head logits.
            return_loss: return the weighted sum of per-head cross entropies.
            return_errors: return a per-head 0/1 error tensor.
            return_error_rate: return the aggregate error rate.

        Returns:
            dict with any of "logits" (list), "loss", "errors" (list), "error_rate".
        """
        assert emb.shape[:-2] == x.shape[:-1], "Leading dimensions of x and emb must match"
        assert emb.shape[-1] == self.d_model, "Embedding last dimension must match d_model"
        assert x.shape[-1] == self.d_model, "Input last dimension must match d_model"
        assert emb.shape[-2] >= self.n_heads - 1, "Embedding must have at least N-1 variables for N heads"
        assert lbl is not None or not (return_loss or return_errors or return_error_rate), "Labels must be provided to compute loss or errors"

        loss_weights = self.loss_weights if self.training else (self.loss_weights_eval or self.loss_weights)

        outputs = {}
        for i in range(self.n_heads):
            x = self.nrm_inp(x)
            logits = self.linear_out[i](x)

            if return_logits:
                outputs.setdefault("logits", []).append(logits)

            if return_errors or return_error_rate:
                pred = logits.argmax(dim=-1)
                error = (pred != lbl[..., i]).float()
                if return_errors:
                    outputs.setdefault("errors", []).append(error)
                if return_error_rate:
                    # divide by the total number of valid labels so the rate stays
                    # correct when some labels are -100
                    error_rate = ((error * (lbl[..., i] != -100).float()).sum()
                                  / ((lbl != -100).float().sum() + 1e-8))
                    outputs["error_rate"] = outputs.get("error_rate", 0) + error_rate

            if return_loss:
                loss_weight = loss_weights[i] if loss_weights is not None else 1.0
                if loss_weight:
                    loss = F.cross_entropy(logits.reshape(-1, logits.shape[-1]),
                                           lbl[..., i].reshape(-1),
                                           ignore_index=-100,
                                           reduction="mean")
                    outputs["loss"] = outputs.get("loss", 0) + loss * loss_weight

            if i < self.n_heads - 1:
                e = emb[..., i, :]
                if self.emb_norm:
                    e = self.nrm_emb(e)
                x = torch.cat([x, e], dim=-1)
                x = self.linear_in[i](x) * F.silu(self.linear_gate[i](x))
        return outputs

    @torch.no_grad()
    def infer(self, embs: nn.ModuleList, x: torch.Tensor,
              top_k: int = 1,
              search_mode: Optional[Literal["beam", "sample", "greedy"]] = None,
              max_k: Optional[List[int]] = None) -> Tuple[torch.Tensor, torch.Tensor]:
        """Return the top-k predicted tuples.

        Args:
            embs: the N-1 embedding modules, one per component that is fed back.
            x: transformer output, shape (*, d_model).
            top_k: number of tuples to return.
            search_mode: "beam" searches over combinations, "greedy" takes the
                best component each step, "sample" draws from each component.
            max_k: per-head cap on candidates during beam search (0 = no cap).

        Returns:
            (ids, logits) of shape (*, E, N) and (*, E), where E <= top_k is the
            beam size that survived the final head.
        """
        if search_mode is None:
            search_mode = self.infer_search_mode or "beam"
        if max_k is not None:
            assert len(max_k) == self.n_heads, "max_k length must match number of heads"
        else:
            max_k = self.infer_max_k

        assert x.shape[-1] == self.d_model, "Input last dimension must match d_model"
        assert search_mode in ["beam", "sample", "greedy"], "search_mode must be 'beam', 'sample' or 'greedy'"

        batch_shape = x.shape[:-1]
        x = x.reshape(-1, self.d_model)  # B x D

        # first head: from the transformer output alone
        k_0 = min(top_k, self.d_heads[0], (max_k[0] if max_k is not None else 0) or top_k)

        x = self.nrm_inp(x)
        y_0 = torch.log_softmax(self.linear_out[0](x), dim=-1)  # B x d_head_0
        if search_mode in ["beam", "greedy"]:
            logits, ids = torch.topk(y_0, k=k_0, dim=-1, largest=True, sorted=True)  # B x k_0
        else:  # sample
            ids = torch.multinomial(torch.exp(y_0), num_samples=k_0, replacement=False)  # B x k_0
            logits = torch.gather(y_0, 1, ids)  # B x k_0

        if self.n_heads == 1:
            return ids.reshape(*batch_shape, k_0, 1), logits.reshape(*batch_shape, k_0)

        E = k_0
        ids = ids.reshape(-1, E, 1)            # B x E x 1
        x = x.unsqueeze(-2).expand(-1, E, -1)  # B x E x D
        for i in range(1, self.n_heads):
            # recursive step: feed back the previous component's embedding
            e = embs[i - 1](ids[..., i - 1])  # B x E x D
            if self.emb_norm:
                e = self.nrm_emb(e)
            x = torch.cat([x, e], dim=-1)  # B x E x 2D
            x = self.linear_in[i - 1](x) * F.silu(self.linear_gate[i - 1](x))
            x = self.nrm_inp(x)

            y_i = torch.log_softmax(self.linear_out[i](x), dim=-1)  # B x E x d_head_i

            if search_mode == "beam":
                k_i = min(top_k, self.d_heads[i], (max_k[i] if max_k is not None else 0) or top_k)
                logits_i, ids_i = torch.topk(y_i.reshape(-1, y_i.shape[-1]), k=k_i,
                                             dim=-1, largest=True, sorted=True)  # (B*E) x k_i
                logits_i = logits_i.reshape(-1, E, k_i)
                ids_i = ids_i.reshape(-1, E, k_i)

                # combine with the running beam
                top_k_i = min(top_k, E * k_i)
                logits = logits.unsqueeze(-1) + logits_i  # B x E x k_i
                logits, idx_i = torch.topk(logits.reshape(-1, E * k_i), k=top_k_i,
                                           dim=-1, largest=True, sorted=True)  # B x top_k_i
                idx_prev = idx_i.unsqueeze(-1) // k_i  # index into E of the previous step

                ids_i = ids_i.reshape(-1, E * k_i)
                ids_prev = torch.gather(ids, 1, idx_prev.expand(-1, -1, ids.shape[-1]))
                ids_next = torch.gather(ids_i, 1, idx_i).unsqueeze(-1)
                ids = torch.cat([ids_prev, ids_next], dim=-1)  # B x top_k_i x (i+1)

                E = top_k_i
                if i < self.n_heads - 1:
                    x = torch.gather(x, 1, idx_prev.expand(-1, -1, x.shape[-1]))

            else:  # sample or greedy
                if search_mode == "sample":
                    ids_i = torch.multinomial(torch.exp(y_i.reshape(-1, y_i.shape[-1])),
                                              num_samples=1, replacement=False)  # (B*E) x 1
                    logits_i = torch.gather(y_i.reshape(-1, y_i.shape[-1]), 1, ids_i)
                else:  # greedy
                    logits_i, ids_i = torch.topk(y_i.reshape(-1, y_i.shape[-1]), k=1,
                                                 dim=-1, largest=True, sorted=True)
                logits_i = logits_i.reshape(-1, E)
                ids_i = ids_i.reshape(-1, E, 1)
                logits = logits + logits_i
                ids = torch.cat([ids, ids_i], dim=-1)

        return ids.reshape(*batch_shape, E, self.n_heads), logits.reshape(*batch_shape, E)
```

This is the production head with the infrastructure stripped out. In a real
training setup you will want to add mixed-precision casts around the
projections, and a fused/chunked cross entropy (the vocabulary logits are the
largest tensor in the model) — neither changes the structure above.

## Wiring it up

```python
class TransformerLM(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.embs = nn.ModuleList([
            nn.Embedding(config.vocab_size, config.d_model),   # vocabulary ids
            nn.Embedding(config.props_size, config.d_model),   # property ids
        ])
        self.layers = ...                                      # your transformer
        self.head = MultiValuedRecursiveHead(
            config.d_model,
            [config.vocab_size, config.props_size],
            loss_weights=(1.0, 1.0),
        )

    def forward(self, input_ids, labels=None):
        # input_ids: (batch, seq, 2)
        x = sum(emb(input_ids[..., i]) for i, emb in enumerate(self.embs))
        x = self.layers(x)

        if labels is None:
            # next-token labels; -100 masks the last position
            labels = input_ids.roll(-1, dims=1)
            labels[:, -1, :] = -100

        # teacher forcing: the head sees the embedding of the true vocab id
        # when predicting the property id
        emb = self.embs[0](labels[..., 0].clamp(min=0)).unsqueeze(-2)

        return self.head(x, emb, labels,
                         return_logits=False, return_loss=True, return_error_rate=True)
```

`emb` carries the components that are fed back, one per head after the first —
shape `(*, N-1, d_model)`. `clamp(min=0)` keeps the masked `-100` positions from
indexing out of bounds; their loss is dropped by `ignore_index` anyway.

## Inference

`infer` returns the top-k *tuples*, not the top-k of each component
independently:

```python
x = model.layers(model.embed(input_ids))[:, -1]      # (batch, d_model)
ids, logits = model.head.infer(model.embs[:1], x, top_k=4, search_mode="beam")
# ids:    (batch, E, 2)  -- E <= top_k surviving candidates
# logits: (batch, E)     -- summed log-probabilities, descending
```

| mode | behaviour |
|---|---|
| `beam` | searches combinations; with a wide enough beam this returns the true joint optimum |
| `greedy` | best component at each step; cheapest, can miss the best tuple |
| `sample` | draws each component from its distribution |

`max_k` caps the candidates per head. A property id has low perplexity once the
vocabulary id is known, so `max_k=[top_k, 4]` costs almost nothing in quality
and keeps the beam small. Note that `top_k=1` makes `beam` identical to
`greedy`, since only one first component survives.

## Packing ids into scalars

Some pipelines want a plain integer per token — a data collator, an existing
embedding layer, an on-disk format. The tuple packs losslessly:

```python
stride = len(tokenizer.model.vocab)

packed = [v_id + stride * p_id for v_id, p_id in ids]          # pack
ids    = [(t % stride, t // stride) for t in packed]           # unpack
```

Two things to watch:

* **The packed id space is huge and must never size an embedding table.** For
  `eu24_96k` it is `98304 * 6 * 2661 = 1,569,521,664`. Unpack first and embed
  each component separately, as in the input-side snippet above.
* **`[PAD]` is vocabulary id 0** in the shipped models, so a packed padding
  value of `0` unpacks to `([PAD], prop 0)` and needs no special handling.

Reserved tokens are in the vocabulary like any other entry — the current models
use `[BOT]`, `[EOT]`, `[PAD]`, `[UNK]`, `[MSK]`, `[CLS]` and 26 `[RSVnnn]`
slots. Older models used `[SOT]` where the current ones use `[BOT]`.

```python
tokenizer.model.vocab_lookup["[BOT]"]
```
