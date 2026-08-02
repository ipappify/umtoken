# How umtoken works

A standard tokenizer maps a word to a sequence of subword ids. umtoken maps it
to a sequence of **tuples**: a vocabulary id plus a property id that carries the
things a subword id should not have to encode — leading whitespace, casing, and
which morphological rule produced the surface form.

The payoff is that one vocabulary entry covers a whole paradigm. `stop`,
`stops`, `stopped`, `stopping` and `stopper` are five separate entries in a BPE
vocabulary; in umtoken they are one entry (`stop`, id 2217) combined with five
different property ids.

The three levels below are cumulative and optional — a tokenizer can be trained
at any of them. The vocabulary and rule ids are the real ones from
`umtoken/assets/eu24_96k.json`, which is a level 3 model; the level 1 table
shows what a level 1 tokenizer would assign for the same word.

## Level 1 — whitespace and case

The tokenizer separates properties (leading whitespace: yes/no; case: lower,
Title, UPPER) from the word itself, so `" Einrichtung"` and `"einrichtung"`
share a vocabulary entry. The property id combines the two:

```
prop_id = ws_id + up_id * 2
```

| word | vocab_id | properties | ws_id | up_id | prop_id | token_id |
|---|---|---|---|---|---|---|
| `"system"` | 950 | ws: no, case: lower | 0 | 0 | 0 + 0·2 = 0 | (950, 0) |
| `" system"` | 950 | ws: yes, case: lower | 1 | 0 | 1 + 0·2 = 1 | (950, 1) |
| `" System"` | 950 | ws: yes, case: Title | 1 | 1 | 1 + 1·2 = 3 | (950, 3) |
| `" SYSTEM"` | 950 | ws: yes, case: UPPER | 1 | 2 | 1 + 2·2 = 5 | (950, 5) |

## Level 2 — suffix rules

The tokenizer separates stems from suffixes via preset rules for the supported
language (`einrichtung` → `einricht+ung`). The rule id joins the property id:

```
prop_id = ws_id + up_id * 2 + rule_id * 6
```

Rule 1 is the identity rule (no suffix); in `eu24_96k` the plural rule `+s` is
rule 1699. These are the ids the shipped model actually assigns:

| word | vocab_id | properties | ws_id | up_id | rule_id | prop_id | token_id |
|---|---|---|---|---|---|---|---|
| `"system"` | 950 | ws: no, case: lower, rule: – | 0 | 0 | 1 | 0 + 0·2 + 1·6 = 6 | (950, 6) |
| `" system"` | 950 | ws: yes, case: lower, rule: – | 1 | 0 | 1 | 1 + 0·2 + 1·6 = 7 | (950, 7) |
| `" System"` | 950 | ws: yes, case: Title, rule: – | 1 | 1 | 1 | 1 + 1·2 + 1·6 = 9 | (950, 9) |
| `" SYSTEM"` | 950 | ws: yes, case: UPPER, rule: – | 1 | 2 | 1 | 1 + 2·2 + 1·6 = 11 | (950, 11) |
| `" System`**`s`**`"` | 950 | ws: yes, case: Title, rule: **+s** | 1 | 1 | 1699 | 1 + 1·2 + 1699·6 = 10197 | (950, 10197) |

You can see this for yourself:

```python
from umtoken import Tokenizer

tokenizer = Tokenizer.load("umtoken/assets/eu24_96k.json")
tokenizer.tokenize(" Systems")                          # [(950, 10197)]
tokenizer.tokenize(" Systems", merge_prop_ids=False)    # [(950, 1699, 1, 1)]
```

`merge_prop_ids=False` returns the unpacked `(vocab_id, rule_id, up_id, ws_id)`
tuple instead of the packed `(vocab_id, prop_id)` pair.

## Level 3 — morphological operations

A rule may carry a regex operation that transforms the base into the stem before
the suffix is appended. That is what lets a single base cover forms with
consonant doubling, `y → i`, or a dropped ending:

| lang | word | base | regex op | suffix | decomposition |
|---|---|---|---|---|---|
| en | `"stopped"` | `stop` | `([bdfgklmnprst])$` → `\1\1` | `+ed` | `sto[p->pp]+ed` |
| en | `"carried"` | `carry` | `y$` → `i` | `+ed` | `carr[y->i]+ed` |
| es | `"veces"` | `vez` | `z$` → `c` | `+es` | `ve[z->c]+es` |
| fr | `"journaux"` | `journal` | `al$` → `` | `+aux` | `journ[al->]+aux` |

Without level 3, `stopped` and `stopping` would each need their own vocabulary
entry (`stopp`) alongside `stop`. With it, all of them resolve to base 2217.

## Reading a decomposition

The human-readable form printed by `format_token_ids` uses three markers:

| marker | meaning |
|---|---|
| `+` | boundary between stem and suffix (`einricht+ung`) |
| `[x->y]` | regex op applied to the base before the suffix (`sto[p->pp]+ed`) |
| trailing `+` | the stem continues into the next token (`schutz+`) |

```python
from umtoken import Tokenizer, format_token_ids

tokenizer = Tokenizer.load("umtoken/assets/eu24_96k.json")
ids = tokenizer.tokenize(" Rechtsschutzversicherung", merge_prop_ids=False)
format_token_ids(ids, tokenizer.model.morpher, no_join=True,
                 apply_ws=True, apply_case=True)
# [' Recht+s', 'schutz+', 'versicher+ungX']
```

`format_token_ids` requires the unpacked tuples — passing packed ids raises
`IndexError`. The `x`/`X` suffix is the end-of-word marker; strip it for display.

## Rules per language

Rules are hand-written per language and live in
[`umtoken/langs/`](../umtoken/langs). Each file documents the paradigms it
covers — see [`de.md`](../umtoken/langs/de.md) for an example.

The effort is manageable: a few common rules per language already give a large
reduction in tokens per word, and if no rule applies the word is simply
tokenized into subwords the usual way. Adding a language does not require
covering its morphology exhaustively.
