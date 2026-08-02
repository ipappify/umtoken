# umtoken vs. a standard BPE tokenizer

Standard tokenizers such as BPE and WordPiece treat leading whitespace, casing
and morphology as part of the string to be split. umtoken treats them as
separate dimensions of a token. This page shows what that changes, side by side.

Every split below was generated from the shipped tokenizers, not written by
hand: umtoken from `umtoken/assets/eu24_96k.json`, GPT-5 from tiktoken's
`o200k_base`. That encoding is shared by the whole GPT-5.x family and by GPT-4o
(see [BENCHMARKS.md](BENCHMARKS.md#gpt-5-is-one-tokenizer-not-several)).

## Compound words

| lang | word | GPT-5 (200k) | umtoken EU-24 (96k) |
|---|---|---|---|
| de | `"Fluorchlorkohlenwasserstoff"` | `"Fl" "u" "orch" "l" "ork" "oh" "len" "wasser" "stoff"` | `"Fluor" "chlor" "kohl+en" "wasserstoff"` |
| fr | `"chlorofluorocarbone"` | `"chlor" "of" "lu" "or" "ocar" "bone"` | `"chlor+o" "fluor+o" "carbon+e"` |
| nl | `"gegevensverwerking"` | `"gegevens" "ver" "werking"` | `"gegeven+s" "verwerk+ing"` |

GPT-5's pieces are mostly meaningless (`"Fl"`, `"lu"`) or carry a meaning
unrelated to the word — `"or"`, `"bone"` in a word about chlorofluorocarbon.
umtoken's pieces are the parts the compound is actually made of.

## Case and whitespace

| lang | word | GPT-5 (200k) | umtoken EU-24 (96k) |
|---|---|---|---|
| de | `"Fluorchlorkohlenwasserstoff"` | `"Fl" "u" "orch" "l" "ork" "oh" "len" "wasser" "stoff"` | `"Fluor" "chlor" "kohl+en" "wasserstoff"` |
| de | `" Fluorchlorkohlenwasserstoff"` | `" Flu" "orch" "l" "ork" "oh" "len" "wasser" "stoff"` | `" Fluor" "chlor" "kohl+en" "wasserstoff"` |
| de | `" FLUORCHLORKOHLENWASSERSTOFF"` | `" FL" "U" "OR" "CH" "L" "ORK" "O" "HL" "EN" "W" "ASS" "ER" "ST" "OFF"` | `" FLUOR" "CHLOR" "KOHL+EN" "WASSERSTOFF"` |
| en | `" runners"` | `" runners"` | `" ru[n->nn]+ers"` |
| en | `"sprinters/runners"` | `"spr" "in" "ters" "/r" "unners"` | `"sprint+ers" "/" "ru[n->nn]+ers"` |

GPT-5 produces three different splits of the same German word depending on
casing and a leading space — 9, 8 and 14 tokens. umtoken produces the same four
vocabulary entries every time; the space and the casing move into the property
id. The last two rows show the same effect at a word boundary: `" runners"` is
one clean token for GPT-5, but the moment it follows a slash it becomes
`"/r" "unners"`, splitting the word in a place that means nothing.

## Word forms

Where umtoken differs most is not always token *count* — it is how many
**vocabulary entries** a paradigm consumes.

| lang | word | GPT-5 (200k) | umtoken EU-24 (96k) |
|---|---|---|---|
| en | `" stop"` | `" stop"` | `" stop"` |
| en | `" stops"` | `" stops"` | `" stop+s"` |
| en | `" stopped"` | `" stopped"` | `" sto[p->pp]+ed"` |
| en | `" stopping"` | `" stopping"` | `" sto[p->pp]+ing"` |
| en | `" stopper"` | `" stopper"` | `" sto[p->pp]+er"` |

Both tokenizers spend exactly one token per form here — English is the language
BPE vocabularies are best at. But GPT-5 spends **five distinct vocabulary
entries** (ids 5666, 29924, 18145, 36616, 154160) on the five forms, and nothing
in those ids tells the model they are related. umtoken spends **one** (id 2217,
base `stop`) plus five property ids. The relationship is in the representation
rather than something the model has to infer from co-occurrence.

The same holds where umtoken also wins on count:

| lang | word | GPT-5 (200k) | umtoken EU-24 (96k) |
|---|---|---|---|
| fr | `" centrifuger"` | `" centrif" "uger"` | `" centrifug+er"` |
| fr | `" centrifugent"` | `" centrif" "ug" "ent"` | `" centrifug+ent"` |
| fr | `" centrifugeant"` | `" centrif" "uge" "ant"` | `" centrifug+eant"` |
| en | `" trimmable"` | `" tr" "imm" "able"` | `" tri[m->mm]+able"` |

Three French verb forms cost GPT-5 six vocabulary entries and 2-3 tokens each,
with a different second piece every time (`"uger"`, `"ug"`, `"uge"`). umtoken
uses one entry (`centrifug`) and one token per form.

## Where a BPE tokenizer holds up

umtoken is not uniformly ahead on every word. `" stop"` and its forms tie on
token count, and a BPE vocabulary trained heavily on English will match or beat
umtoken on common English words that happen to be single tokens. The advantage
shows up in aggregate, and it grows with morphological richness — see the
per-language numbers in [BENCHMARKS.md](BENCHMARKS.md#results), where the gap
runs from +5% on English to +72% on Greek.

## Reproducing any row

```python
import tiktoken
from umtoken import Tokenizer, format_token_ids

enc = tiktoken.get_encoding("o200k_base")
tok = Tokenizer.load("umtoken/assets/eu24_96k.json")

word = " centrifugeant"
print([enc.decode([i]) for i in enc.encode(word)])

ids = tok.tokenize(word, merge_prop_ids=False)
print(format_token_ids(ids, tok.model.morpher, no_join=True,
                       apply_ws=True, apply_case=True))
```
