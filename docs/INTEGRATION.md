# Integrating umtoken into a model

umtoken does not return a scalar token id but a tuple of vocabulary id and
property id. A transformer has to be adapted to accept those tuples on the input
side and to produce them on the output side.

This page shows how, in PyTorch. If you only want to tokenize text, you do not
need any of it — see the quick start in the [README](../README.md#quick-start).

## Embedding and projection

The example uses 2-tuples `(vocab_id, property_id)`. When a language has many
rules — as the Slavic languages do — 3-tuples
`(vocab_id, rule_id, ws_id + 2 * up_id)` tend to work better, because they let
the model generalize to rule/case combinations it has not seen.

```python
import math
import torch
import torch.nn as nn
import torch.nn.functional as F

# ...

class TransformerLM(nn.Module):
    def __init__(self, config):
        super().__init__()
        # setup layers etc.
        # ...

        # setup embeddings and projections
        model_dim = config.model_dim # dimension of the model
        model_low = min(1024, config.model_dim) # (optional) it's usually ok to reduce model_dim for projection of props if model_dim is large
        vocab_size = config.vocab_size # number of vocab ids
        props_size = config.props_size # number of rule ids * 3 (for cases) * 2 (for ws)

        self.emb_0 = nn.Embedding(vocab_size, model_dim)
        self.emb_1 = nn.Embedding(props_size, model_dim)
        self.prj_0 = nn.Linear(model_dim, vocab_size)
        self.prj_1 = nn.Linear(model_low, props_size)
        self.prj_linear = nn.Linear(2 * model_dim, model_low) # Gated Linear Unit (GLU) for autoregressive projection of props
        self.prj_gate = nn.Linear(2 * model_dim, model_low)

        # init weights the usual way
        # ...

    def forward(self, input_ids, labels=None):
        # the following code assumes that input_ids have a further dimension to accommodate the 2-tuples of vocab id and property id
        # e.g. (batch_size, seq_len, **2**)
        input_ids_0 = input_ids[..., 0]
        input_ids_1 = input_ids[..., 1]

        # if input_ids are packed into scalars, we need to unpack them:
        # e.g. input_ids_0 = input_ids % vocab_size, input_ids_1 = input_ids // vocab_size

        # embed: simply add embeddings
        x = self.emb_0(input_ids_0) + self.emb_1(input_ids_1)

        # apply transformer layers to x
        y = self.layers(x)

        # project to vocab: first, project to vocab (y_0)
        y_0 = self.prj_0(y)

        # the following code assumes training where we have labels or at least the complete input sequence
        if labels is None:
            # left-shift input_ids along sequence dim to obtain labels if not provided
            labels_0 = input_ids_0.roll(-1, dims=1) # assuming shape (batch_size, seq_len)
            labels_0[:,-1] = -100                   # mask last token, assuming -100 is used for loss masking

        # at inference, we would sample from y_0 first and use the result as labels_0
        # e.g. labels_0 = torch.argmax(y_0, dim=-1)
        # for top-k projection (required for beam search), see below

        # project to props: use GLU to merge transformer output y and vocab embedding x_0 for autoregressive projection to props (y_1)
        y_m = torch.cat((y, self.emb_0(labels_0.clamp(min=0))), dim=-1) # clamp to avoid negative indices (loss masking)
        y_m = self.prj_linear(y_m) * F.silu(self.prj_gate(y_m))
        y_1 = self.prj_1(y_m)

        # compute output (log_softmax/argmax over y_0 and y_1, loss, etc.)
        output = self.compute_output(y_0, y_1, labels)
        return output

    def project_topk(self, y, k, k_1 = None):
        # here is an example of how to project the model output for top-k sampling during inference.

        # the basic idea is to sample k vocab ids first, then combine them with the model output to sample k_1 prop ids.
        # finally, top-k samples are taken from the combined logits of vocab and props.
        # because shuffling dimensions and indexes is always a bit confusing, the example is intentionally kept verbose.
        # note that k_1 = 4 is more than enough for props, since props usually have low perplexity given the vocab id.
        # (we still use k_1 = k if not set).

        # assuming shape (batch_size, seq_len, model_dim),
        # where seq_len is the length of the current output and is usually 1 during inference
        B, T, C = y.shape

        # make sure there is no out-of-bounds error
        k_0 = min(k, config.vocab_size)
        k_1 = min(k_1 or k, config.props_size)

        # project to vocab: (B, T, C) -> (B, T, vocab_size)
        y_0 = self.prj_0(y)
        y_0 = F.log_softmax(y_0, dim=-1)

        # top-k sampling with k_0: (B, T, vocab_size) -> (B, T, k_0), (B, T, k_0)
        logits_0, ids_0 = torch.topk(y_0, k=k_0, dim=-1)

        # expand model ouput: (B, T, C) -> (B, T, k_0, C) -> (B*T*k_0, C)
        y = y.view(B, T, 1, C).expand(-1, -1, k_0, -1).reshape(-1, C)

        # embed vocab ids of top-k tokens: (B, T, k_0) -> (B*T*k_0,) -> (B*T*k_0, C)
        e_0 = self.emb_0(ids_0.view(-1))

        # concatenate model output and vocab embeddings: (B*T*k_0, C), (B*T*k_0, C) -> (B*T*k_0, 2*C)
        y_m = torch.cat((y, e_0), dim=-1)

        # apply GLU and project to props: (B*T*k_0, 2*C) -> (B*T*k_0, props_size)
        y_m = self.prj_linear(y_m) * F.silu(self.prj_gate(y_m))
        y_1 = self.prj_1(y_m)
        y_1 = F.log_softmax(y_1, dim=-1)

        # top-k sampling with k_1: (B*T*k_0, props_size) -> (B*T*k_0, k_1), (B*T*k_0, k_1)
        logits_1, ids_1 = torch.topk(y_1, k=k_1, dim=-1)

        # expand top-k vocab ids: (B, T, k_0) -> (B, T, k_0, k_1) -> (B*T, k_0*k_1)
        logits_0 = logits_0.view(B, T, k_0, 1).expand(-1, -1, -1, k_1).reshape(B*T, -1)
        ids_0 = ids_0.view(B, T, k_0, 1).expand(-1, -1, -1, k_1).reshape(B*T, -1)

        # reshape top-k prop ids: (B*T*k_0, k_1) -> (B*T, k_0*k_1)
        logits_1 = logits_1.view(B*T, k_0 * k_1)
        ids_1 = ids_1.view(B*T, k_0 * k_1)

        # sum and reshape logits: (B*T, k_0*k_1), (B*T, k_0*k_1) -> (B, T, k_0*k_1)
        logits = (logits_0 + logits_1).view(B, T, k_0 * k_1)
        # stack and reshape ids: (B*T, k_0*k_1), (B*T, k_0*k_1) -> (B, T, k_0*k_1, 2)
        ids = torch.stack([ids_0, ids_1], dim=2).view(B, T, k_0 * k_1, 2)

        # finally, take top-k samples: (B, T, k_0*k_1) -> (B, T, k), (B, T, k)
        k = min(k, k_0 * k_1)
        logits, idxs = torch.topk(logits, k=k, dim=-1)
        # and get ids at idxs: (B, T, k_0*k_1, 2), (B, T, k) -> (B, T, k, 2)
        ids = torch.gather(ids, dim=-2, index=idxs.unsqueeze(-1).expand(-1, -1, -1, 2))

        # return top-k logits and ids: (B, T, k), (B, T, k, 2)
        # the last dimension of ids is the 2-tuple of vocab id and prop id
        return logits, ids
```

## Hugging Face wrapper

A preliminary wrapper is available in the `umtoken.hf` module. `UnimorphTokenizer`
implements `PreTrainedTokenizerBase` and is compatible with the `transformers`
library — models still need the adaptations above.

```python
from umtoken.hf import UnimorphTokenizer

tokenizer = UnimorphTokenizer.from_pretrained("umtoken/assets/eu24_96k.json",
                                              force_slow=True)
ids = tokenizer.encode("Hello, my dog is cute.", add_special_tokens=False)
tokenizer.decode(ids)
```

By default the wrapper packs the 2-tuple `(v_id, p_id)` into a scalar integer
(`len(vocab) * p_id + v_id`). A `PreTrainedModel` then has to unpack the scalar
input ids and repack the output where necessary.

To set a prefix and suffix token — note that the current models use `[BOT]`, not
the `[SOT]` of older ones:

```python
tokenizer.set_prefix("[BOT]")
tokenizer.set_suffix("[EOT]")
```

`transformers` is an optional dependency; install it if you want the wrapper:

```bash
pip install transformers
```
