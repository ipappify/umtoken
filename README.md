# Unimorph Tokenizer (umtoken)

**A tokenizer for morphologically rich languages.** umtoken factorizes words
into tuples of *vocabulary entry* and *properties* — leading whitespace, casing,
and the morphological rule that produced the surface form — instead of splitting
them into subword strings. The result is fewer tokens per word, a smaller
vocabulary, and pieces that mean something.

Here is the French word for chlorofluorocarbon under a standard BPE tokenizer
([try it yourself](http://tokenizers.ipappify.de/)):

| | `"chlorofluorocarbone"` |
|---|---|
| OpenAI GPT-5 (200k vocab) | `"chlor"` `"of"` `"lu"` `"or"` `"ocar"` `"bone"` |
| **umtoken EU-24 (96k vocab)** | `"chlor+o"` `"fluor+o"` `"carbon+e"` |

😕 *the chlor of what bone 🦴? lu or ocar?*

For English and Chinese this rarely matters. For the inflected and agglutinative
languages of Europe it matters a lot: subwords differ between forms of the same
word, they are often meaningless, and they change depending on casing and
leading whitespace. Longer token sequences also cost memory and compute, and the
usual remedy — an ever larger vocabulary — spends parameters on the embedding
and projection layers instead of on the model.

## How well it works

![Words per token by language family](assets/words_per_token_by_family.png)

Measured on 66 GB of Wikipedia text across the 24 official EU languages:

> **umtoken needs the fewest tokens in all 24 languages**, at a *smaller*
> vocabulary than any of the tokenizers it is compared against. GPT-5 needs
> **22%** more tokens for the same text, Gemma 4 **27%**, Qwen3.6 **30%**.

It is also far more even across languages. GPT-5 costs 1.16 tokens per word in
English but 2.17 in Greek — a spread of **1.86x**, which carries straight
through to context limits, latency and per-token pricing. umtoken ranges from
1.10 to 1.31, a spread of **1.18x**.

| tokenizer | vocab | tokens/word | spread across languages |
|---|---:|---:|---:|
| **umtoken EU-24** | **96k** | **1.150** | **1.18x** |
| OpenAI GPT-5 | 200k | 1.403 | 1.86x |
| Google Gemma 4 | 262k | 1.467 | 1.90x |
| Alibaba Qwen3.6 | 248k | 1.494 | 1.88x |

Per-language numbers, method and reproduction: **[docs/BENCHMARKS.md](docs/BENCHMARKS.md)**.

## Quick start

```bash
git clone https://github.com/ipappify/umtoken.git
pip install -e ./umtoken
```

```python
from umtoken import Tokenizer, format_token_ids

tokenizer = Tokenizer.load("umtoken/assets/eu24_96k.json")

ids = tokenizer.tokenize("Die Rechtsschutzversicherung zahlt nicht.")
len(ids)                      # 7  -- GPT-5 needs 8, Gemma 4 needs 8, Qwen3.6 needs 9
tokenizer.detokenize(ids)     # 'Die Rechtsschutzversicherung zahlt nicht.'
```

`tokenize` returns `(vocab_id, prop_id)` pairs. To see the decomposition, ask
for the unpacked tuples — `format_token_ids` needs them and raises `IndexError`
on packed ids:

```python
ids = tokenizer.tokenize(" Rechtsschutzversicherung", merge_prop_ids=False)
format_token_ids(ids, tokenizer.model.morpher, no_join=True,
                 apply_ws=True, apply_case=True)
# [' Recht+s', 'schutz+', 'versicher+ungX']
```

`+` marks a stem/suffix boundary, a trailing `+` means the stem continues into
the next token, and the `x`/`X` at the end is the end-of-word marker.

## Pretrained models

Under [`assets/`](assets):

| model | vocab | rules | languages | trained on |
|---|---:|---:|---|---|
| [`eu24_96k.json`](assets/eu24_96k.json) | 96k | 2661 | all 24 official EU languages | nllb + clean-wikipedia + Wiktionary forms |
| [`ipt_32k.json`](assets/ipt_32k.json) | 32k | 212 | de, en, fr | patent text |

`k` denotes 1024, not 1000.

## How it works

Three cumulative levels, each optional at training time:

| level | what it separates | `" Einrichtung"` becomes |
|---|---|---|
| 1 | leading whitespace and casing | `einrichtung` + *(ws: yes, case: Title)* |
| 2 | \+ suffix rules | `einricht+ung` + *(ws: yes, case: Title, rule: +ung)* |
| 3 | \+ morphological operations | `sto[p->pp]+ed` for `"stopped"`, from base `stop` |

Because the properties are a separate dimension, one vocabulary entry covers a
whole paradigm. `stop`, `stops`, `stopped`, `stopping` and `stopper` are five
distinct entries in GPT-5's vocabulary; in umtoken they are **one** entry
(`stop`) plus five property ids.

Full explanation with the property-id encoding: **[docs/HOW-IT-WORKS.md](docs/HOW-IT-WORKS.md)**.

## What this changes

* **Pieces are meaningful.** `"Fluorchlorkohlenwasserstoff"` →
  `"Fluor" "chlor" "kohl+en" "wasserstoff"`, not
  `"Fl" "u" "orch" "l" "ork" "oh" "len" "wasser" "stoff"`.
* **Casing and whitespace do not change the tokens.** GPT-5 splits that same
  German word three different ways (9, 8 and 14 tokens) depending on a leading
  space and casing; umtoken yields the same four entries every time.
* **Word forms stay consistent.** `centrifuger` / `centrifugent` /
  `centrifugeant` cost GPT-5 six vocabulary entries and a different second piece
  each time; umtoken uses one entry and one token per form.

Side-by-side tables for all three: **[docs/COMPARISON.md](docs/COMPARISON.md)**.

## Supported languages

Morphological rules are available for all 24 official EU languages. Each links
to its rule documentation:

[bg](umtoken/langs/bg.md) · [cs](umtoken/langs/cs.md) · [da](umtoken/langs/da.md) ·
[de](umtoken/langs/de.md) · [el](umtoken/langs/el.md) · [en](umtoken/langs/en.md) ·
[es](umtoken/langs/es.md) · [et](umtoken/langs/et.md) · [fi](umtoken/langs/fi.md) ·
[fr](umtoken/langs/fr.md) · [ga](umtoken/langs/ga.md) · [hr](umtoken/langs/hr.md) ·
[hu](umtoken/langs/hu.md) · [it](umtoken/langs/it.md) · [lt](umtoken/langs/lt.md) ·
[lv](umtoken/langs/lv.md) · [mt](umtoken/langs/mt.md) · [nl](umtoken/langs/nl.md) ·
[pl](umtoken/langs/pl.md) · [pt](umtoken/langs/pt.md) · [ro](umtoken/langs/ro.md) ·
[sk](umtoken/langs/sk.md) · [sl](umtoken/langs/sl.md) · [sv](umtoken/langs/sv.md)

Adding a language is not a large effort. A handful of common rules already gives
most of the reduction, and words that match no rule are tokenized into subwords
the usual way.

## Documentation

| | |
|---|---|
| [docs/BENCHMARKS.md](docs/BENCHMARKS.md) | EU-24 results, method, how to reproduce |
| [docs/HOW-IT-WORKS.md](docs/HOW-IT-WORKS.md) | levels 1-3 and the property-id encoding |
| [docs/COMPARISON.md](docs/COMPARISON.md) | umtoken vs. BPE, side by side |
| [docs/INTEGRATION.md](docs/INTEGRATION.md) | adapting a PyTorch model; Hugging Face wrapper |
| [docs/TOOLS.md](docs/TOOLS.md) | `extract.py`, `train.py`, `test.py`, `eval.py` |
| <http://tokenizers.ipappify.de/> | try it in the browser |

## About

umtoken is a rewrite of the [IP.Translator](https://www.ipappify.de/en/ip-translator)
tokenizer that IP.appify has used for its translation models since 2021, cleaned
up and with some design flaws fixed. It is based on a modified unigram model.

**A note on performance.** umtoken is pure Python, with help from numpy and
marisa-trie. The lattice algorithm, rule engine and EM training are written for
readability and flexibility rather than speed. That is a deliberate trade: the
time to train a tokenizer and tokenize a corpus is negligible next to training a
language model. Prefix tries keep it reasonably efficient regardless, and
multiprocessing or caching will speed it up further if you need it.

## Contributing

There is no contribution guide yet. Please get in touch if you would like to
contribute.

## License

See [LICENSE](LICENSE).
