# Path: umtoken/trainer.py

import os
import regex as re
from collections import Counter
from typing import Dict, List, Optional, Tuple, Union
from multiprocessing import Pool
from time import sleep

import numpy as np
from tqdm import tqdm

from .alphabet import (EU3_ALPHABET, ASCII_RESERVED_EOW, ASCII_ENCODING_SHY,
                       ASCII_ENCODING_NEWLINE, ASCII_ENCODING_SPACE, ASCII_ENCODING_TAB, 
                       ASCII_RESERVED_UTF8, ASCII_ENCODING)
from .pre import DEFAULT_RESERVED_TOKENS, UNK_TOKEN
from .model import Model, MIN_LOGIT
from .rules import MorphRule
from .utils import chunk_list

DEFAULT_NUMBER_SEED = [f"{d:01}" for d in range(0, 10)] + [f"{d:02}" for d in range(0, 100)] + ["000"] # add 0-9, 00-99, 000
DEFAULT_WS_SEED = sum(([ASCII_ENCODING_SPACE * (2**i), 
                        ASCII_ENCODING_NEWLINE * (2**i), 
                        ASCII_ENCODING_TAB * (2**i)] for i in range (0, 4)), [])
DEFAULT_MARKUP_SEED = sum((["#" * (2**i), 
                            "=" * (2**i), 
                            "-" * (2**i), 
                            "+" * (2**i), 
                            "*" * (2**i),
                            "_" * (2**i)] for i in range (0, 4)), [])
# 21-7E should be covered by the alphabet (uppercase letters are only used as special tokens)
# we need to add the first byte of multi-byte sequences (1 1 0 x x x x x, 1 1 1 0 x x x x, 1 1 1 1 0 x x x)
# and the next byte(s) (1 0 x x x x x x)
DEFAULT_UTF8_SEED = (
    [ASCII_RESERVED_UTF8 + f"{i+192:02X}" for i in range(2**5)] + # multi-byte start: 110xxxxx = 192
    [ASCII_RESERVED_UTF8 + f"{i+224:02X}" for i in range(2**4)] + # multi-byte start: 1110xxxx = 224
    [ASCII_RESERVED_UTF8 + f"{i+240:02X}" for i in range(2**3)] + # multi-byte start: 11110xxx = 240
    [ASCII_RESERVED_UTF8 + f"{i+128:02X}" for i in range(2**6)]   # multi-byte continuation: 10xxxxxx = 128
)

DEFAULT_ALPHA = 1.0
DEFAULT_BETA = 0.02

class TrainerConfig():
    def __init__(self, 
                 vocab_size: int = 24 * 1024, 
                 alphabet: str = EU3_ALPHABET,
                 escape_chars: str = ASCII_ENCODING,
                 reserved_tokens: List[str] = DEFAULT_RESERVED_TOKENS,
                 unk_token: str = UNK_TOKEN,
                 spread_factor: float = 16,
                 max_token_length: int = 12,
                 token_regex: Optional[str] = None,
                 discount_exponent: float = 1.0,
                 min_count: int = 1,
                 seed_tokens: List[str] = DEFAULT_NUMBER_SEED + DEFAULT_WS_SEED + DEFAULT_MARKUP_SEED + DEFAULT_UTF8_SEED,
                 seed_token_logit: Optional[float] = 0.0,
                 skip_numbers: bool = True,
                 iterations: int = 10,
                 alpha: float = DEFAULT_ALPHA,
                 beta: float = DEFAULT_BETA,
                 min_base_len: int = 2,
                 tie_by_langs: bool = False,
                 min_balance_langs: Optional[float] = None,
                 workers: int = 0,
                 force_slow: bool = False
                 ):
        """unimorph trainer configuration.
        
        Args:
            vocab_size: The size of the vocabulary.
            alphabet: The alphabet to use.
            escape_chars: The escape characters.
            reserved_tokens: The reserved tokens.
            unk_token: The unknown token.
            spread_factor: The spread factor for the candidate generation.
            max_token_length: The maximum length of a token.
            token_regex: Only candidate tokens matching this regex are extracted.
            discount_exponent: The discount exponent for word frequencies.
            min_count: The minimum count for a word to be considered.
            seed_tokens: The seed tokens which are guaranteed to be included in the vocabulary.
            seed_token_logit: The logit for seed tokens (default: 0).
            skip_numbers: Whether to skip numbers (default: True).
            iterations: The number of iterations to run.
            alpha: Vocab logits are multiplied with alpha (default: DEFAULT_ALPHA).
            beta: Rule logits are multiplied with beta (default: DEFAULT_BETA).
            min_base_len: Minimum length of a base (default: 2).
            tie_by_langs: Whether to tie vocab and rules by langs.
            min_balance_langs: Lower bound for balance among languages (default: None). 
                               If the sum of word counts for a language is less than 
                               this value times the sum of word counts over the dominant language, 
                               the word counts will be upsampled to meet this condition. 
            workers: The number of workers to use for parallelization (<1: use as many works as cpus).
            force_slow: Force slow mode to prevent building a stem trie (=pretransformed bases).
                        Note that each worker needs to build its own trie. If the number of workers is high,
                        it may be preferrable to use force_slow=True to prevent building the stem trie.
        """
        assert iterations > 1

        self.vocab_size = vocab_size
        self.alphabet = alphabet
        self.reserved_tokens = reserved_tokens
        self.escape_chars = escape_chars
        self.unk_token = unk_token
        self.spread_factor = spread_factor
        self.max_token_length = max_token_length
        self.token_regex = token_regex
        self.discount_exponent = discount_exponent
        self.min_count = min_count
        self.seed_tokens = seed_tokens or []
        self.seed_token_logit = seed_token_logit
        self.skip_numbers = skip_numbers
        self.iterations = iterations
        self.alpha = alpha
        self.beta = beta
        self.min_base_len = min_base_len
        self.tie_by_langs = tie_by_langs
        self.min_balance_langs = min_balance_langs
        self.workers = workers if workers > 0 else os.cpu_count()
        self.force_slow = force_slow

class Trainer():
    def __init__(self, config: TrainerConfig):
        self.config = config

        # reserved tokens must be added first, then add unique alphabet and seed tokens
        self.protected_tokens_list = list(self.config.reserved_tokens)
        protected_tokens = set(self.protected_tokens_list)
        assert len(protected_tokens) == len(self.protected_tokens_list), "Duplicate tokens in reserved tokens"
        for token in list(self.config.escape_chars) + list(self.config.alphabet) + self.config.seed_tokens:
            if token not in protected_tokens:
                self.protected_tokens_list.append(token)
                protected_tokens.add(token)
        self.protected_tokens = frozenset(self.protected_tokens_list)
        assert len(self.protected_tokens) == len(self.protected_tokens_list), "Duplicate tokens in protected tokens"

    def train(self, 
              rules: List[MorphRule],
              words: Optional[Dict[str, Union[int, float]]],
              words_by_lang: Optional[Dict[str, Dict[str, Union[int, float]]]],
              eval_words: Optional[List[str]] = None):
        """
        Train the unimorph model.
        
        Args:
            rules: The morphological rules.
            words: The words.
            words_by_lang: The words by language.
            eval_words: The evaluation words.
        """
        assert words is not None or words_by_lang is not None, "Either words or words_by_lang must be provided"
        
        langs = list(sorted(set([l for r in rules for l in r.langs or [] if not r.any_lang]) | 
                            set((words_by_lang or {}).keys())))
        words, lang_by_words = self.prepare_words(words, words_by_lang)
        
        print("Building initial candidates")
        candidates = self.generate_candidates(words)
        candidates.update(self.protected_tokens)
        prune_rate = 1 - (len(candidates) / self.config.vocab_size) ** (-1.0 / (self.config.iterations - 1))
        
        final = False
        for it in range(self.config.iterations):
            print(f'it={it}')
            
            model = Model(candidates, rules,
                          [0.0] * len(candidates), 
                          [0.0] * len(rules),
                          self.config.alpha, self.config.beta,
                          langs=langs,
                          min_base_len=self.config.min_base_len)
            model.reset_logits()
            
            # EM
            for subit in range(3 if final else 2):
                nll, m_vocab, m_rules = self.step_E(model, words, lang_by_words)
                self.step_M(model, m_vocab, m_rules)
                print(f'  NLL({subit})={nll}')           
                 
            # eval
            self.eval_model(model, eval_words)
            
            # prune
            if final:
                # update progress bar properly
                if it == self.config.iterations - 1:
                    continue
                else:
                    break
            prune_count = min(int(len(model.vocab) * prune_rate), len(model.vocab) - self.config.vocab_size)
            if it == self.config.iterations - 2 or prune_count == 0:
                prune_count = len(model.vocab) - self.config.vocab_size
                final = True
            
            if prune_count > 0:
                remove = self.prune(model, words, lang_by_words, prune_count)
                candidates = candidates - remove
                print(f'  pruned {len(remove)} tokens ({len(candidates)} left)')
        self.finalize_model(model)
        
        if self.config.tie_by_langs:
            self.tie_model(model, words, lang_by_words)
            self.eval_model(model, eval_words)
            untied = sum(1 for l in model.vocab_langs[len(self.protected_tokens):] if l == 0)
            print(f"Untied vocab: {untied}")
        
        print('done')
        return model
        
    def prepare_words(self, words, words_by_lang):
        """
        Prepare the words:
        - balance word counts among languages, if necessary.
        - remove protected tokens (reserved + seed + alphabet).
        - strip soft-hyphens (encoded as 'H' and indicated word continuation, e.g. modifier in compound words).
        - otherwise, append end-of-word marker 'X'.
        
        Args:
            words: The words.
            words_by_lang: The words by language.
            
        Returns:
            A tuple of he prepared words and their languages.
        """
        eow = ASCII_RESERVED_EOW
        shy = ASCII_ENCODING_SHY
        
        # balance word counts between languages
        words = Counter(words or dict())
        if words_by_lang:
            if self.config.min_balance_langs:
                count_by_langs = Counter({lang: sum(words_by_lang[lang].values()) for lang in words_by_lang})
                _, dominant_count = count_by_langs.most_common(1)[0]
                for lang, lang_words in words_by_lang.items():
                    lang_factor = 1.0
                    lang_count = count_by_langs[lang]
                    if lang_count < self.config.min_balance_langs * dominant_count:
                        lang_factor = self.config.min_balance_langs * dominant_count / lang_count
                    print(f"Upsampling {lang} by factor {lang_factor}")
                    for word in lang_words:
                        if word in self.config.reserved_tokens:
                            continue
                        words[word] += lang_words[word] * lang_factor # float is ok here
            else:
                for lang, lang_words in words_by_lang.items():
                    words += Counter(lang_words)
        
        # filter and discount
        for word in list(words.keys()):
            count = words.pop(word)
            if count < self.config.min_count:
                continue
            if word == "":
                continue
            if word in self.protected_tokens:
                continue
            if self.config.skip_numbers and word.isdigit():
                continue
            count = count ** self.config.discount_exponent
            words[word] = count

        # get primary language for each word
        words = list(words.items())
        lang_by_words = [None] * len(words) # None means all languages
        if self.config.tie_by_langs:
            # get primary language for each word
            for i, (word, _) in enumerate(words):
                lang_counts = Counter()
                for lang in words_by_lang:
                    lang_counts[lang] = words_by_lang[lang].get(word, 0)
                if len(lang_counts) > 1:
                    lang = lang_counts.most_common(1)[0][0]
                    lang_by_words[i] = lang
                else:
                    lang_by_words[i] = None
                    
        # remove soft-hyphens, add end-of-word marker
        for i, (word, count) in enumerate(words):    
            if len(word) > 1 and word[-1] == shy:
                words[i] = word[:-1], count
            else:
                words[i] = word + eow, count

        return words, lang_by_words
    
    def generate_candidates(self, words):
        """
        Generate candidates.
        
        Args:
            words: The words.
            
        Returns:
            The candidates.
        """
        token_regex = re.compile(self.config.token_regex) if self.config.token_regex is not None else None
        candidates = Counter()
        for word, count in words:
            # avoid dangling end-of-word markers
            word_len = len(word) - 1 if word.endswith(ASCII_RESERVED_EOW) else len(word)
            for i in range(word_len):
                for j in range(i + 2, min(i + self.config.max_token_length, word_len) + 1):
                    token = word[i:j]
                    if token_regex and not token_regex.match(token):
                        continue
                    candidates[token] += count
        return set(t for t, _ in candidates.most_common(self.config.vocab_size * self.config.spread_factor))
    
    def step_E(self, model: Model, words: List[Tuple[str, float]], lang_by_words: List[Optional[str]]):
        return step_E(model, words, lang_by_words, self.config.workers, self.config.force_slow)
    
    def step_M(self, model: Model, m_vocab, m_rules):
        model.update_logits(m_vocab, m_rules)
        # TODO: apply special logit rules here

    def prune(self, model: Model, words: List[Tuple[str, float]], langs_by_words: List[Optional[set]], prune_count: int):
        unused = frozenset(v for v, l in zip(model.vocab, model.vocab_logits) if l <= MIN_LOGIT) - self.protected_tokens
        if len(unused) > prune_count:
            remove = unused
        else:
            losses = compute_losses(model, words, langs_by_words, self.config.workers, self.config.force_slow)
            losses = sorted([(l, v) for v, l in zip(model.vocab, losses) if v not in self.protected_tokens])
            remove = frozenset(v for _, v in losses[0:prune_count])
        return remove
    
    def eval_model(self, model: Model, eval_words: List[str]):
        if not eval_words:
            return
        print(f'evaluating model (vocab={len(model.vocab)}):')
        for word in eval_words:
            p = model.encode(word, force_slow=True)
            p = ' | '.join([model.format_token(*a) for a in p])
            print(f'{word}: {p}')

    def finalize_model(self, model: Model):
        token_order = {v: i for i, v in enumerate(self.protected_tokens_list)}
        vocab_order = {(token_order.get(v, 1000000 - model.vocab_logits[model.vocab_lookup[v]]), i) for i, v in enumerate(model.vocab)}
        vocab_order = [i for _, i in sorted(vocab_order)]
        model.rearrange_vocab(vocab_order)
        model.vocab_logits[:len(self.config.reserved_tokens)] = 0.0
        model.unk_token_id = model.vocab_lookup[self.config.unk_token]
        # override seed token logits
        if self.config.seed_token_logit is not None:
            for token in self.config.seed_tokens:
                model.vocab_logits[model.vocab_lookup[token]] = self.config.seed_token_logit
        
    def tie_model(self, model: Model, words: List[Tuple[str, float]], langs_by_words: List[Optional[set]]):
        vocab_langs = tie(model, words, langs_by_words, self.config.workers, self.config.force_slow)
        for i in range(len(self.protected_tokens)):
            vocab_langs[i] = (1 << len(model.langs)) - 1
        model.update_tied_langs(model.langs, vocab_langs)
    
def step_E_single(model: Model, words: List[Tuple[str, float]], langs_by_words: List[Optional[set]], show_progress: bool, force_slow: bool):
    m_vocab = [0.0] * len(model.vocab)
    m_rules = [0.0] * len(model.rules)
    nll = 0.0
    total_count = 0
    for (word, count), lang in tqdm(zip(words, langs_by_words), desc=f'step E', total=len(words), disable=not show_progress):
        # force_slow to prevent building stem trie
        nll -= model.add_marginal(word, count, lang, m_vocab, m_rules, force_slow=force_slow)
        total_count += count
    nll /= total_count
    return nll, m_vocab, m_rules
    
def step_E(model: Model, words: List[Tuple[str, float]], lang_by_words: List[Optional[str]], workers: int, force_slow: bool):
    if workers == 1:
        return step_E_single(model, words, lang_by_words, show_progress=True, force_slow=force_slow)
    word_chunks = chunk_list(words, workers)
    lang_chunks = chunk_list(lang_by_words, workers)
        
    with Pool(workers) as p:
        results = [p.apply_async(step_E_single, (model, cw, cl, i==0, force_slow)) 
                   for i, (cw, cl) in enumerate(zip(word_chunks, lang_chunks))]
        while any(not r.ready() for r in results):
            sleep(0.1)

        nll = 0.0
        total = 0
        m_vocab = [0.0] * len(model.vocab)
        m_rules = [0.0] * len(model.rules)
        for result, chunk in zip(results, word_chunks):
            _nll, _m_vocab, _m_rules = result.get()
            _total = sum(c for _, c in chunk)
            nll += _nll * _total
            total += _total
            add_arrays(m_vocab, _m_vocab)
            add_arrays(m_rules, _m_rules)

        nll /= total
        return nll, m_vocab, m_rules

def compute_losses_single(model: Model, words: List[Tuple[str, float]], lang_by_words: List[Optional[str]], show_progress: bool, force_slow: bool):
    losses = [0.0] * len(model.vocab)
    for (word, count), lang in tqdm(zip(words, lang_by_words), desc=f'pruning', total=len(words), disable=not show_progress):
        model.add_vocab_loss(word, count, lang, losses, force_slow=force_slow)
    return losses

def compute_losses(model: Model, words: List[Tuple[str, float]], lang_by_words: List[Optional[str]], workers: int, force_slow: bool):
    if workers == 1:
        return compute_losses_single(model, words, lang_by_words, show_progress=True, force_slow=force_slow)
    word_chunks = chunk_list(words, workers)
    langs_chunks = chunk_list(lang_by_words, workers)

    with Pool(workers) as p:
        results = [p.apply_async(compute_losses_single, (model, cw, cl, i==0, force_slow)) 
                   for i, (cw, cl) in enumerate(zip(word_chunks, langs_chunks))]
        while any(not r.ready() for r in results):
            sleep(0.1)

        losses = [0.0] * len(model.vocab)
        for result in results:
            _losses = result.get()
            add_arrays(losses, _losses)

        return losses

def tie_single(model: Model, words: List[Tuple[str, float]], lang_by_words: List[Optional[str]], show_progress: bool, force_slow: bool):
    langs = model.langs
    langs_map = {l: i for i, l in enumerate(langs)}
    vocab_langs = [0] * len(model.vocab) # don't care about memory consumption here
    for (word, _), lang in tqdm(zip(words, lang_by_words), desc=f'tie by langs', total=len(words), disable=not show_progress):
        ids = model.encode(word, lang, force_slow=force_slow, eow_applied=True)
        lang_mask = 1 << langs_map[lang] if lang else (1 << len(langs)) - 1
        for v_id, _ in ids:
            vocab_langs[v_id] |= lang_mask
    return vocab_langs

def tie(model: Model, words: List[Tuple[str, float]], lang_by_words: List[Optional[str]], workers: int, force_slow: bool):
    if workers == 1:
        return tie_single(model, words, lang_by_words, show_progress=True, force_slow=force_slow)
    word_chunks = chunk_list(words, workers)
    langs_chunks = chunk_list(lang_by_words, workers)

    with Pool(workers) as p:
        results = [p.apply_async(tie_single, (model, cw, cl, i==0, force_slow)) 
                   for i, (cw, cl) in enumerate(zip(word_chunks, langs_chunks))]
        while any(not r.ready() for r in results):
            sleep(0.1)

        vocab_langs = [0] * len(model.vocab)
        for result in results:
            _vocab_langs = result.get()
            for i in range(len(vocab_langs)):
                vocab_langs[i] |= _vocab_langs[i]
        return vocab_langs


def add_arrays(a, b):
    for i in range(len(a)):
        a[i] += b[i]
