# Command line tools

Four modules, run in this order when training a tokenizer from scratch:

```
extract.py  →  train.py  →  test.py / eval.py
 corpus         vocabulary    inspect / measure
 → vocabulary   → tokenizer
```

You only need these to train your own tokenizer. To use a pretrained one, see
the quick start in the [README](../README.md#quick-start).

## Extract vocabulary (`extract.py`)

Counts words in the input files and writes a vocabulary file.

```bash
python -m umtoken.extract -i <input_path> -c <column_name> -o <output_path> [-l <regex_pattern>]
```

| option | meaning |
|---|---|
| `-i`, `--input-file` | input file(s); supports wildcards (`~/data/super_eurlex/*/*_clean.parquet`) |
| `-c`, `--column-name` | column(s) holding the text (e.g. `text_cleaned`) |
| `-o`, `--output-file` | where the vocabulary is written; `{lang}` is substituted |
| `-n`, `--normalization` | unicode normalization: `default`, `ipt`, `ipt-cjk`, `nfc` (default: `default`) |
| `-f`, `--min-frequency` | minimum frequency for a word to be kept |
| `-lr`, `--lang-regex` | regex extracting the language code from the filename; group 1 is used |
| `-lc`, `--lang-column-name` | column holding the language; one column, or one per `--column-name` |

Depending on the file type you may need extra packages — `polars` for parquet,
`pyzstd` for zstd-compressed input:

```bash
pip install polars datasets pyzstd
```

**Example.** Download a corpus — here
[`ddrg/super_eurlex`](https://huggingface.co/datasets/ddrg/super_eurlex), EU
legislation and jurisdiction in the 24 official languages:

```bash
huggingface-cli download --repo-type dataset --local-dir ~/data/super_eurlex ddrg/super_eurlex --include "**/*_clean.parquet"
```

Extract per language, using the filename to identify each:

```bash
python -m umtoken.extract -i "~/data/super_eurlex/*/*_clean.parquet" -c "text_cleaned" -l ".(\\w{2}).\\w+_clean.parquet" -o "~/data/super_eurlex/{lang}.vocab.json"
```

Or a single language:

```bash
python -m umtoken.extract -i "~/data/super_eurlex/BG/*_clean.parquet" -c "text_cleaned" -o "~/data/super_eurlex/bg.vocab.json"
```

## Train tokenizer (`train.py`)

Trains a tokenizer from the extracted vocabularies.

```bash
python -m umtoken.train -i <lang_vocab_pairs> -c <cache_dir> -l <languages> -v <vocab_size> [-mc <min_word_count>] [-mb <min_base_length>] [-t] [-o <output_path>]
```

| option | meaning |
|---|---|
| `-i`, `--input-file` | language-to-vocabulary mappings (`en:~/data/en.vocab.json`) |
| `-o`, `--output-file` | where the trained tokenizer is written |
| `-c`, `--cache-dir` | cache directory for intermediate files |
| `-e`, `--eval-file` | eval file(s), one word per line (txt) |
| `-v`, `--vocab-size` | vocabulary size (e.g. `24576`) |
| `-mc`, `--min-count` | minimum count for a word to be included (default: 1) |
| `-mb`, `--min-base-len` | minimum base length for applying rules (default: 2) |
| `-ml`, `--min-balance-langs` | minimum upsampling per language, relative to the dominant one (default: 0.5) |
| `-rp`, `--rule-penalty` | penalty for non-default rules (default: -0.4) |
| `-d`, `--discount-exponent` | exponent for discounting word frequencies (default: 1.0) |
| `-l`, `--languages` | languages to include (e.g. `eu3`) |
| `-t`, `--tie` | tie vocabulary and rules by language |
| `-n`, `--normalization` | `default`, `ipt`, `ipt-cjk`, `nfc` (default: `default`) |
| `-w`, `--workers` | worker count; 0 = one per CPU (default: 0) |
| `-its`, `--iterations` | number of EM iterations (default: 10) |
| `--no-rules` | use only the necessary default rules |
| `--no-constraints` | do not apply constraints to rules |
| `--no-penalties` | do not apply penalties to rules |
| `--no-ops` | do not use rules with morphological operations (level 2) |
| `--allow-unconditional-ops` | allow rules with unconditional morphological operations |

**Example.** A 24k tokenizer for English, German and French:

```bash
python -m umtoken.train -i "en:~/data/super_eurlex/en.vocab.json" "de:~/data/super_eurlex/de.vocab.json" "fr:~/data/super_eurlex/fr.vocab.json" -in -c "~/data/super_eurlex/cache" -l "eu3" -v 24576 -mc 3 -d "0.7" -t -o "~/data/super_eurlex/tokenizers/eu3_24k_tied.json"
```

## Test tokenizer (`test.py`)

Tokenizes a word list and prints the result in human-readable form — the quickest
way to see what a trained tokenizer does.

```bash
python -m umtoken.test -t <tokenizer_path> -i <input_path>
```

| option | meaning |
|---|---|
| `-t` | path to the trained tokenizer |
| `-i` | input file(s), one word per line |

```bash
python -m umtoken.test -t "~/data/super_eurlex/tokenizers/eu3_24k_tied.json" -i "~/data/test/en.txt"
```

## Evaluate tokenizer (`eval.py`)

Computes tokens-per-word per language and writes them to a file. This is what
produces the umtoken column in [BENCHMARKS.md](BENCHMARKS.md).

```bash
python -m umtoken.eval -i <lang_vocab_pairs> -t <tokenizer_path> -o <output_path>
```

| option | meaning |
|---|---|
| `-i`, `--input-file` | language-to-vocabulary mappings |
| `-t`, `--tokenizer-file` | path to the trained tokenizer |
| `-o`, `--output-file` | where the results are written |
| `-ot`, `--output-tokenized-file` | also write the tokenized words (jsonl) |
| `-of`, `--output-formatted-file` | also write the formatted tokenized words (txt) |
| `-w`, `--workers` | worker count; 0 = one per CPU (default: 0) |
| `-c`, `--check` | check that tokenization is reversible |

```bash
python -m umtoken.eval -i "en:~/data/super_eurlex/en.vocab.json" "de:~/data/super_eurlex/de.vocab.json" "fr:~/data/super_eurlex/fr.vocab.json" -t "~/data/super_eurlex/tokenizers/eu3_24k_tied.json" -o "~/data/super_eurlex/eval/eu3_24k_tied.json"
```
