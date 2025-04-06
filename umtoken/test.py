# Path: umtoken/test.py

import argparse

from .tokenizer import Tokenizer
from .utils import format

def main(args):
    assert len(args.input_file) > 0, "No input files specified."

    tokenizer = Tokenizer.load(args.tokenizer_file)
    for input_file in args.input_file:
        with open(input_file, 'r', encoding="utf8") as f:
            if input_file.endswith('.txt'):
                words = open(input_file, 'r', encoding="utf8").read().splitlines()
            else:
                raise ValueError("Unsupported input file format.")
            for word in words:
                ids = tokenizer.tokenize(word, merge_prop_ids=False, force_slow=True)
                tokens = []
                for v_id, r_id, _, _ in ids:
                    token = format([(v_id, r_id)], tokenizer.model.morpher)
                    tokens.append(token)
                print(f"{word} > {' '.join(tokens)}")

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="Evaluate a tokenizer.")
    
    parser.add_argument("-i", "--input-file", 
                        nargs="+",
                        required=True,
                        help="input file(s) containing one word per line (txt).")

    parser.add_argument("-t", "--tokenizer-file",
                        required=True,
                        help="tokenizer file to evaluate (json)")

    args = parser.parse_args()
    main(args)
