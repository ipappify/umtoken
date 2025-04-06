import os
import regex as re
import argparse
import json
import hashlib
from collections import Counter
from typing import List

from tqdm import tqdm

from .alphabet import get_alphabet
from .pre import PreTokenizer
from .trainer import Trainer, TrainerConfig
from .langs import get_rules
from .tokenizer import Tokenizer
from .utils import expand_languages

def main(args):
    assert len(args.input_file) > 0, "No input files specified."
    assert len(args.languages) > 0, "No languages specified."
    assert args.normalization in ["default", "ipt", "nfc"], "Unsupported normalization."
    
    languages: List[str] = args.languages
    expand_languages(languages)
    alphabet = get_alphabet(languages)

    # config
    config = TrainerConfig(
        vocab_size=args.vocab_size,
        min_count=args.min_count,
        discount_exponent=args.discount_exponent,
        workers=args.workers,
        tie_by_langs=args.tie,
        iterations=args.iterations,
        alphabet=alphabet,
        min_balance_langs=args.min_balance_langs,
        min_base_len=args.min_base_len,        
        force_slow=args.allow_unconditional_ops # building the stem trie may take a long time when there are unconditional ops
    )
    trainer = Trainer(config)
    pre = PreTokenizer(alphabet=config.alphabet, 
                       reserved_tokens=config.reserved_tokens, 
                       normalization=args.normalization)
    rules = get_rules(languages if not args.no_rules else [], 
                      drop_constraints=args.no_constraints, 
                      drop_penalties=args.no_penalties,
                      remove_op_rules=args.no_ops,
                      remove_unconditional_op_rules=not args.allow_unconditional_ops,
                      add_penalties=args.rule_penalty)
    
    print(f"Training tokenizer with {len(rules)} rules and {len(config.alphabet)} characters.")
    if config.tie_by_langs:
        print(f"- with lang tying")
    if args.no_constraints:
        print(f"- without constraints")
    if args.no_penalties:
        print(f"- without penalties")
    if args.no_ops:
        print(f"- without morph ops")
    if args.allow_unconditional_ops:
        print(f"- with unconditional morph ops")
    if args.no_rules:
        print(f"- without rules")
    
    def normalize(word):
        # see extract.py
        word = pre.normalize(word)
        word = word.strip(" ") if len(word) > 1 else word
        word = word.lower()
        return word
    
    loaded_from_cache = False
    if args.cache_dir:
        key = f"{args.normalization}--{config.alphabet}--{'|'.join(args.input_file)}"
        key_hash = hashlib.md5(key.encode()).hexdigest()
        words_cache_file = os.path.join(args.cache_dir, f"words--{key_hash}.json")
        if os.path.exists(words_cache_file):
            with open(words_cache_file, 'r', encoding="utf8") as f:
                words, words_by_langs = json.load(f)
                loaded_from_cache = True

    if not loaded_from_cache:
        # read word counts from input files
        words = Counter()
        words_by_langs = {}
        for input_file in tqdm(args.input_file, desc="Reading input files"):
            input_lang = None
            if re.match(r'[a-z]{2}:', input_file):
                input_lang, input_file = input_file.split(':', 1)
                assert input_lang in args.languages, f"Input file {input_file} is not contained in the specified languages."

            with open(input_file, 'r', encoding="utf8") as f:
                if input_file.endswith('.jsonl'):
                    counter = dict(tuple(json.loads(l)) for l in f)
                elif input_file.endswith('.json'):
                    counter= json.load(f)
                else:
                    raise ValueError("Unsupported input file format.")
                if not args.input_normalized:
                    counter = {normalize(w): c for w, c in counter.items()}
                if not args.input_encoded:
                    counter = {pre.encoding.escape(w): c for w, c in counter.items()}
                if not input_lang:
                    words += Counter(counter)
                else:
                    words_by_langs[input_lang] = words_by_langs.get(input_lang, Counter()) + Counter(counter)
                    
        if args.cache_dir:
            os.makedirs(args.cache_dir, exist_ok=True)
            with open(words_cache_file, 'w', encoding="utf8") as f:
                json.dump([words, words_by_langs], f, ensure_ascii=False, indent=None)

    # load eval words
    eval_words = []
    if args.eval_file:
        for eval_file in args.eval_file:
            with open(eval_file, 'r', encoding="utf8") as f:
                eval_words.extend(f.read().splitlines())
        eval_words = [normalize(w) for w in eval_words]
        eval_words = [pre.encoding.escape(w) for w in eval_words]
                
    # train
    model = trainer.train(rules=rules, words=words, words_by_lang=words_by_langs, eval_words=eval_words)

    # build and save the tokenizer
    thumbprint = model.thumbprint()
    tokenizer = Tokenizer(pre, model, thumbprint=thumbprint)
    os.makedirs(os.path.dirname(args.output_file), exist_ok=True)
    tokenizer.save(args.output_file)    


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="Train a new tokenizer from word counts.")
    
    parser.add_argument("-i", "--input-file", 
                        nargs="+",
                        required=True,
                        help="input file(s) containing columns 'word' and 'count' (json ot jsonl). May be of the form lang:file.")

    parser.add_argument("-o", "--output-file",
                        required=True,
                        help="output file to save the trained tokenizer to (json)")
    
    parser.add_argument("-e", "--eval-file", 
                        nargs="+",
                        help="eval file(s) containing a word in each line (txt).")
    
    parser.add_argument("-c", "--cache-dir",
                        help="cache directory to store intermediate results")
    
    parser.add_argument("-v", "--vocab-size",
                        default=24*1024,
                        type=int,
                        help="size of vocabulary to train (default: 24*1024)")
    
    parser.add_argument("-in", "--input-normalized", 
                        action="store_true",
                        help="input words are already normalized (default: False)")
    
    parser.add_argument("-ie", "--input-encoded", 
                        action="store_true",
                        help="input words are already encoded (default: False)")
    
    parser.add_argument("-mc", "--min-count",
                        default=1,
                        type=int,
                        help="minimum count of a word to be included in the vocabulary (default: 1)")
    
    parser.add_argument("-mb", "--min-base-len",
                        default=2,
                        type=int,
                        help="minimum length of a base for applying rules (default: 2)")
    
    parser.add_argument("-ml", "--min-balance-langs",
                        default=0.5,
                        type=float,
                        help="minimum counts to upsample each language to, relative to the dominant language (default: 0.5)")
    
    parser.add_argument("-rp", "--rule-penalty",
                        default=-0.4,
                        type=float,
                        help="penalty for non-default rules (default: -0.4), > 0: penalize rules, < 0: reward rules, takes precedence over --no-penalties")
    
    parser.add_argument("-d", "--discount-exponent",
                        default=1.0,
                        type=float,
                        help="exponent for discounting word frequencies (default: 1.0)")
    
    parser.add_argument("-l", "--languages",
                        default=["eu3"],
                        nargs="+",
                        help="languages to train for (default: eu3)")
    
    parser.add_argument("-t", "--tie",
                        action="store_true",
                        help="tie vocabs and rules by languages (default: False)")
    
    parser.add_argument("-n", "--normalization",
                        choices=["default", "ipt", "nfc"],
                        default="default",
                        help="unicode normalization to apply to input words (default: default)")
    
    parser.add_argument("-nr", "--no-rules",
                        action="store_true",
                        help="use only necessary default rules (default: False)")
    
    parser.add_argument("-nc", "--no-constraints",
                        action="store_true",
                        help="do not apply constraints to rules (default: False)")
    
    parser.add_argument("-np", "--no-penalties",
                        action="store_true",
                        help="do not apply penalties to rules (default: False)")
    
    parser.add_argument("-no", "--no-ops",
                        action="store_true",
                        help="do not apply rules with morphological ops (default: False)")
    
    parser.add_argument("-au", "--allow-unconditional-ops",
                        action="store_true",
                        help="allow rules with unconditional morphological ops (default: False)")
    
    parser.add_argument("-w", "--workers",
                        default=0,
                        type=int,
                        help="number of workers; 0 = as many as cpus (default: 0)")
    
    parser.add_argument("-its", "--iterations",
                        default=10,
                        type=int,
                        help="number of iterations (default: 10)")   

    args = parser.parse_args()
    main(args)
