# Path: umtoken/dry_run.py

import os
import argparse
from collections import Counter
from glob import glob

from tqdm import tqdm

from .extract import get_data_iter
from .tokenizer import Tokenizer

def main(args):
    input_files = [f for file in args.input_file for f in glob(file)]
    column_names = args.column_name
    tokenizer_file = args.tokenizer_file
    
    tokenizer = Tokenizer.load(tokenizer_file)
    unk_id = tokenizer.model.unk_token_id
    
    count_unknowns = 0
    count_errors = 0
    count_slow_mismatches = 0
    count_text_mismatches = 0
    count_normalized_mismatches = 0
    
    for input_file in input_files:
        data_iter = get_data_iter(input_file, column_names)
        data_iter = tqdm(data_iter, desc=f"Tokenizing cols {','.join(column_names)} from {input_file}")
        for text in data_iter:
            try:
                ids = tokenizer.tokenize(text, force_slow=False)
                if args.slow:
                    ids_slow = tokenizer.tokenize(text, force_slow=True)
                    if ids != ids_slow:
                        count_slow_mismatches += 1                    
                if any(v_id == unk_id for v_id, _ in ids):
                    count_unknowns += 1
                    continue
                actual = tokenizer.detokenize(ids)
                if text != actual:
                    count_text_mismatches += 1
                    if tokenizer.pre.normalize(text).lower() != actual.lower():
                        count_normalized_mismatches += 1
            except:
                count_errors += 1
            data_iter.desc = f"Tokenizing cols {','.join(column_names)} from {input_file} (unk={count_unknowns} err={count_errors} slw-mis={count_slow_mismatches} txt-mis={count_text_mismatches} nrm-mis={count_normalized_mismatches})"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-file", nargs="+", help="The input file(s). Supported formats: parquet or, (gzipped) jsonl, csv, or txt", required=True)
    parser.add_argument("-c", "--column-name", nargs="+", help="Column name(s) to extract from the input file(s).")
    parser.add_argument("-t", "--tokenizer-file", help="The tokenizer to check", required=True)
    parser.add_argument("-s", "--slow", action="store_true", help="Check slow tokenization against fast tokenization")
    args = parser.parse_args()
    main(args)