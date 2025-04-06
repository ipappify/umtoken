# Path: umtoken/eval.py

import os
import regex as re
import argparse
import json
from collections import Counter
from multiprocessing import Pool
from time import sleep
from typing import List, Tuple

from tqdm import tqdm

from .tokenizer import Tokenizer
from .utils import format, chunk_list

def process_single(words: List[Tuple[str, int]], 
                   tokenizer: Tokenizer, 
                   need_ids: bool, 
                   check: bool, 
                   show_progress: bool, 
                   progress_message: str) -> Tuple[int, int, dict]:
    
    ids_by_words = {}
    word_count = 0
    token_count = 0
    for word, count in tqdm(words, desc=progress_message, disable=not show_progress):
        token_ids = tokenizer.tokenize(word, merge_prop_ids=False)
        if need_ids:
            # save only vocab and rule ids
            ids_by_words[word] = [(v_id, r_id) for v_id, r_id, _, _ in token_ids]
        if check:
            detokenized = tokenizer.detokenize(token_ids)
            if word != detokenized:
                print(f"Tokenization is not reversible: {word} -> {token_ids} -> {detokenized}")
        word_count += count
        token_count += len(token_ids) * count
    return word_count, token_count, ids_by_words

def main(args):
    assert len(args.input_file) > 0, "No input files specified."

    tokenizer = Tokenizer.load(args.tokenizer_file)
    need_ids = args.output_tokenized_file or args.output_formatted_file
    workers = args.workers
    if workers <= 0:
        workers = os.cpu_count()

    # read words or word counts from input files
    ids_by_words = {}
    words_by_langs = Counter()
    tokens_by_langs = Counter()
    for input_file in args.input_file:
        input_lang = "n/a"
        if re.match(r'[a-z]{2}:', input_file):
            input_lang, input_file = input_file.split(':', 1)

        with open(input_file, 'r', encoding="utf8") as f:
            if input_file.endswith('.jsonl'):
                counter = Counter(dict(tuple(json.loads(l)) for l in f))
            elif input_file.endswith('.json'):
                counter = Counter(json.load(f))
            elif input_file.endswith('.txt'):
                counter = Counter(open(input_file, 'r', encoding="utf8").read().splitlines())
            else:
                raise ValueError("Unsupported input file format.")
            
            if workers == 1:
                results = [process_single(counter.items(), tokenizer, need_ids, 
                                          args.check, True, f"Processing {input_file}")]
            else:
                chunks = chunk_list(list(counter.items()), workers)
                with Pool(workers) as p:
                    results = [p.apply_async(process_single, (c, tokenizer, need_ids, args.check, i==0, f"Processing {input_file}")) 
                               for i, c in enumerate(chunks)]
                    while any(not r.ready() for r in results):
                        sleep(0.1)
                    results = [r.get() for r in results]
                        
            for word_count, token_count, ids in results:
                words_by_langs[input_lang] += word_count
                tokens_by_langs[input_lang] += token_count
                ids_by_words.update(ids)
            
            # for word, count in tqdm(counter.items(), desc=f"Processing {input_file}"):
            #     token_ids = tokenizer.tokenize(word, merge_aux_ids=False)
            #     if need_ids:
            #         # save only vocab and rule ids
            #         ids_by_words[word] = [(v_id, r_id) for v_id, r_id, _, _ in token_ids]
            #     if args.check:
            #         detokenized = tokenizer.detokenize(token_ids)
            #         if word != detokenized:
            #             print(f"Tokenization is not reversible: {word} -> {token_ids} -> {detokenized}")
            #     words_by_langs[input_lang] += count
            #     tokens_by_langs[input_lang] += len(token_ids) * count

    os.makedirs(os.path.dirname(args.output_file), exist_ok=True)
    with open(args.output_file, 'w', encoding="utf8") as f:
        results = {}
        for lang in words_by_langs.keys():
            tokens_per_word = tokens_by_langs[lang] / words_by_langs[lang]
            results[lang] = {
                "tokens_per_word": tokens_per_word,
                "words": words_by_langs[lang],
                "tokens": tokens_by_langs[lang]
            }
        json.dump(results, f, ensure_ascii=False, indent=2)

    if args.output_tokenized_file:
        os.makedirs(os.path.dirname(args.output_tokenized_file), exist_ok=True)
        with open(args.output_tokenized_file, 'w', encoding="utf8") as f:
            for word, token_ids in ids_by_words.items():
                json.dump([word, list(token_ids)], f, ensure_ascii=False)
                f.write('\n')

    if args.output_formatted_file:
        os.makedirs(os.path.dirname(args.output_formatted_file), exist_ok=True)
        with open(args.output_formatted_file, 'w', encoding="utf8") as f:
            for word, token_ids in ids_by_words.items():
                f.write(format(token_ids, tokenizer.model.morpher))
                f.write('\n')
        

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="Evaluate a tokenizer.")
    
    parser.add_argument("-i", "--input-file", 
                        nargs="+",
                        required=True,
                        help="input file(s) containing columns 'word' and 'count' (json ot jsonl) or one word per line (txt). May be of the form lang:file.")

    parser.add_argument("-o", "--output-file",
                        required=True,
                        help="output file to save the eval results to (json)")
    
    parser.add_argument("-ot", "--output-tokenized-file",
                        help="output file to save the tokenized words to (jsonl)")
    
    parser.add_argument("-of", "--output-formatted-file",
                        help="output file to save the formatted tokenized words to (txt)")
    
    parser.add_argument("-t", "--tokenizer-file",
                        required=True,
                        help="tokenizer file to evaluate (json)")
    
    parser.add_argument("-w", "--workers",
                        default=0,
                        type=int,
                        help="number of workers; 0 = as many as cpus (default: 0) - CURRENTLY NOT IMPLEMENTED")
    
    parser.add_argument("-c", "--check",
                        action="store_true",
                        help="check the whether tokenization is reversible")

    args = parser.parse_args()
    main(args)
