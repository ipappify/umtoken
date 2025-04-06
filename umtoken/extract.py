# Path: umtoken/extract.py

import os
import argparse
import json
import csv
import gzip
import bz2
import regex as re
from collections import Counter
from glob import glob

from tqdm import tqdm

from .vocab import extract_vocab, save_vocab

def boradcast_lang_cols(cols, lang_cols):
    assert len(lang_cols) in [1, len(cols)], "length of language columns must be 1 or equal to the number of text columns."
    return [lang_cols[0]] * len(cols) if len(lang_cols) == 1 else lang_cols

def iter_nested_list(nested_list):
    for item in nested_list:
        if isinstance(item, list):
            yield from iter_nested_list(item)
        else:
            yield item

def iter_parquet(file, cols, lang_cols=None):
    try:
        import polars as pl
    except ImportError:
        raise ImportError("The parquet format requires the polars library.")
    dataset = pl.read_parquet(file)
    if not lang_cols:
        for col in cols:
            for text in dataset[col]:
                yield text
    else:
        lang_cols = boradcast_lang_cols(cols, lang_cols)
        for col, lang_col in zip(cols, lang_cols):
            for text, lang in dataset[[col, lang_col]].rows():
                yield text, lang
            
def iter_dataset(dir, cols, lang_cols=None):
    try:
        import datasets as ds
    except ImportError:
        raise ImportError("The arrow format requires the pyarrow library.")
    dataset = ds.load_from_disk(dir)
    if not lang_cols:
        for col in cols:
            for text in dataset[col]:
                yield text
    else:
        lang_cols = boradcast_lang_cols(cols, lang_cols)
        for col, lang_col in zip(cols, lang_cols):
            for text, lang in dataset[[col, lang_col]].rows():
                yield text, lang        
            
def iter_jsonl(file, cols, lang_cols=None):
    with open_maybe_zipped(file) as f:
        if not lang_cols:
            for line in f:
                record = json.loads(line)
                for col in cols:
                    yield from iter_nested_list(record[col])
        else:
            lang_cols = boradcast_lang_cols(cols, lang_cols)
            for line in f:
                record = json.loads(line)
                for col, lang_col in zip(cols, lang_cols):
                    lang = record[lang_col]
                    for text in iter_nested_list(record[col]):
                        yield text, lang
    
def iter_csv(file, cols, lang_cols=None):
    with open_maybe_zipped(file) as f:
        reader = csv.DictReader(f)
        if not lang_cols:
            for row in reader:
                for col in cols:
                    yield row[col]
        else:
            lang_cols = boradcast_lang_cols(cols, lang_cols)
            for row in reader:
                for col, lang_col in zip(cols, lang_cols):
                    yield row[col], row[lang_col]
    
def open_maybe_zipped(file):
    if file.endswith(".gz"):
        return gzip.open(file, "rt", encoding="utf8")
    elif file.endswith(".bz2"):
        return bz2.open(file, "rt", encoding="utf8")
    elif file.endswith(".zst"):
        try:
            import pyzstd
        except ImportError:
            raise ImportError("The zstd format requires the pyzstd library.")
        return pyzstd.open(file, "rt", encoding="utf8")
    return open(file, "r", encoding="utf8")

def extract(input_files, cols, lang_cols, normalization, min_frequency):
    if not lang_cols:
        vocab = Counter()    
        for input_file in input_files:
            file_iter = get_data_iter(input_file, cols, lang_cols)
            vocab.update(extract_vocab(file_iter, normalization, min_frequency))
        return vocab
    else:
        vocabs = {}
        for input_file in input_files:
            file_iter = tqdm(get_data_iter(input_file, cols, lang_cols), desc=f"Extracting vocabulary from {input_file}...")
            for text, lang in file_iter:
                if not text or not lang:
                    continue
                vocabs.setdefault(lang, Counter()).update(extract_vocab([text], normalization, min_frequency, progress=False))
        return vocabs

def get_data_iter(input_file, cols, lang_cols):
    if input_file.endswith(".gz"):
        input_ext = os.path.splitext(input_file[:-3])[1]
    elif input_file.endswith(".bz2"):
        input_ext = os.path.splitext(input_file[:-4])[1]
    elif input_file.endswith(".zst"):
        input_ext = os.path.splitext(input_file[:-4])[1]
    else:
        input_ext = os.path.splitext(input_file)[1]
            
    assert os.path.isdir(input_file) or input_ext in [".parquet", ".jsonl", ".csv", ".txt"], f"Unsupported input file format: {input_ext}"
    assert input_ext == ".txt" or cols, "Column name(s) must be provided for non-txt input files."
        
    file_iter = None
    if input_ext == ".parquet":
        file_iter = iter_parquet(input_file, cols, lang_cols)
    elif os.path.isdir(input_file):
        file_iter = iter_dataset(input_file, cols, lang_cols)
    elif input_ext == ".jsonl":
        file_iter = iter_jsonl(input_file, cols, lang_cols)
    elif input_ext == ".csv":
        file_iter = iter_csv(input_file, cols, lang_cols)
    elif input_ext == ".txt":
        assert not cols, "Column names are not supported for txt files."
        assert not lang_cols, "Lang column names are not supported for txt files."
        file_iter = open_maybe_zipped(input_file)
    else:
        raise ValueError(f"Unsupported input file format: {input_ext}")
    return file_iter

def main(args):
    output_file = args.output_file
    input_files = [f for file in args.input_file for f in glob(file)]
    column_names = args.column_name
    normalization = args.normalization
    min_frequency = args.min_frequency
    lang_regex = args.lang_regex
    lang_column_names = args.lang_column_name
    
    assert not lang_regex or not lang_column_names, "Cannot use both lang-regex and lang-column-name options."
    assert len(lang_column_names) in [0, 1, len(column_names)], "lang-column-name must be a single column, or one column for each column in --column-name."
    
    if lang_regex:
        if "{lang}" not in output_file:
            raise ValueError("The output file must contain the {lang} placeholder when using the lang-regex option.")
        
        lang_regex = re.compile(lang_regex)
        files_by_lang = {}
        for input_file in input_files:
            lang_match = lang_regex.search(input_file)
            if lang_match:
                lang = lang_match.group(1).lower()
                if lang not in files_by_lang:
                    files_by_lang[lang] = []
                files_by_lang[lang].append(input_file)
            else:
                raise ValueError(f"Could not extract lang from path: {input_file}")

        for lang, lang_files in files_by_lang.items():
            print(f"Extracting vocab for {lang}...")
            vocab = extract(lang_files, column_names, None, normalization, min_frequency)
            lang_output_file = output_file.replace("{lang}", lang)
            os.makedirs(os.path.dirname(lang_output_file), exist_ok=True)
            save_vocab(vocab, lang_output_file)
    
    elif lang_column_names:
        if "{lang}" not in output_file:
            raise ValueError("The output file must contain the {lang} placeholder when using the lang-regex option.")
        
        vocab_by_lang = extract(input_files, column_names, lang_column_names, normalization, min_frequency)
        for lang, vocab in vocab_by_lang.items():
            lang_output_file = output_file.replace("{lang}", lang)
            os.makedirs(os.path.dirname(lang_output_file), exist_ok=True)
            save_vocab(vocab, lang_output_file)
    
    else:
        vocab = extract(input_files, column_names, None, normalization, min_frequency)
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        save_vocab(vocab, output_file)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-file", nargs="+", help="The input file(s). Supported formats: parquet or, (gzipped) jsonl, csv, or txt", required=True)
    parser.add_argument("-c", "--column-name", nargs="+", help="Column name(s) to extract from the input file(s).")
    parser.add_argument("-n", "--normalization", default="default", choices=["default", "ipt", "nfc"], help="unicode normalization to apply to input words (default: default).")
    parser.add_argument("-f", "--min-frequency", type=int, help="The minimum frequency of a word to be included in the vocabulary.")
    parser.add_argument("-o", "--output-file", help="The output vocab file in json format (compact and fast) or jsonl format (more human readable).", required=True)
    parser.add_argument("-lr", "--lang-regex", help="Regex for extracting lang from path. The first group is used to replace the {lang} placeholder in output file.")
    parser.add_argument("-lc", "--lang-column-name", nargs="+", help="Column name containing the lang in the input file. Maybe a single column, or one column for each column in --column-name.")
    args = parser.parse_args()
    main(args)