# Path: umtoken/model.py 

import hashlib
from base64 import b64encode
from typing import List, Optional, Tuple, Union

import numpy as np

from .alphabet import ASCII_RESERVED_EOW as EOW, ASCII_ENCODING_SHY as SHY
from .rules import MorphRule, SuffixRule
from .morpher import Morpher
from .lattice import Lattice
from .utils import format, get_rules_bitmask

MIN_LOGIT = -20.0
CUTOFF = 1E-3
SHIFT = 1E-5 # tie-breaking for ambiguous paths

def digamma(x):
    "digamma function assumes x > 0."
    r = 0
    while (x <= 5):
        r -= 1 / x
        x += 1
    f = 1 / (x * x)
    t = f * (-1/12.0 + f * (1/120.0 + f * (-1/252.0 + f * (1/240.0 + f * (-1/132.0 + 
        f * (691/32760.0 + f * (-1/12.0 + f * 3617/8160.0)))))))
    return r + np.log(x) - 0.5 / x + t

class Model():
    def __init__(self, 
                 vocab: List[str], 
                 rules: List[MorphRule], 
                 vocab_logits: Union[List[float], np.ndarray],
                 rules_logits: Union[List[float], np.ndarray],
                 alpha: float,
                 beta: float,
                 unk_token_id: int = 0,
                 min_base_len: int = 2,
                 prebuild_stem_trie: bool = False,
                 langs: Optional[List[str]] = None,
                 vocab_langs: Optional[List[int]] = None
                 ):
        """
        A morphological tokenizer model.
        
        Args:
            vocab: The vocabulary.
            rules: The morphological rules.
            vocab_logits: The vocabulary logits.
            rules_logits: The rules logits.
            alpha: The vocabulary weight.
            beta: The rules weight.
            unk_token_id: The unknown token id.
            min_base_len: The minimum base length.
            prebuild_stem_trie: Whether to prebuild the stem trie.
            langs: The languages.
            vocab_langs: The vocabulary languages.
        """
        assert not vocab_langs or langs, "vocab_langs requires langs"
        self.vocab = list(vocab)
        self.rules = list(rules)
        self.langs = list(langs) if langs else list(sorted(set(l for r in rules for l in r.langs or [] if l)))
        self.alpha = alpha
        self.beta = beta
        self.unk_token_id = unk_token_id
        self.min_base_len = min_base_len
        self.vocab_logits = np.array(vocab_logits, dtype=np.float32) if isinstance(vocab_logits, list) else vocab_logits 
        self.rules_logits = np.array(rules_logits, dtype=np.float32) if isinstance(rules_logits, list) else rules_logits

        assert self.vocab_logits.shape == (len(vocab),), "vocab and vocab_logits must have the same length"
        assert self.rules_logits.shape == (len(rules),), "rules and rules_logits must have the same length"
        
        self.vocab_lookup = {v: i for i, v in enumerate(vocab)}
        self.is_eow_rule = [isinstance(r, SuffixRule) and r.suffix.endswith(EOW) for r in rules]
        self.vocab_langs = None
        self.rules_langs = None
        if vocab_langs:
            self.morpher = None
            self.update_tied_langs(langs, vocab_langs)
            
        self.morpher = Morpher(self.langs, self.vocab, self.rules, 
                               min_base_length=min_base_len, prebuild_stem_trie=prebuild_stem_trie,
                               vocab_langs=self.vocab_langs, rules_langs=self.rules_langs)
        
    def _normalize(self, logits):
        logsum = digamma(sum(l for l in logits if l >= CUTOFF))
        for i in range(len(logits)):
            logits[i] = max(digamma(logits[i]) - logsum if logits[i] >= CUTOFF else MIN_LOGIT, MIN_LOGIT)
        return np.array(logits, dtype=np.float32)
    
    def reset_logits(self):
        """Reset the logits to uniform."""
        vocab_count = len(self.vocab)
        rules_count = len(self.rules)
        self.vocab_logits = np.zeros(vocab_count, dtype=np.float32) - np.log(vocab_count)
        self.rules_logits = np.zeros(rules_count, dtype=np.float32) - np.log(rules_count)
    
    def update_logits(self, m_vocab: np.ndarray, m_rules: np.ndarray):
        """Update the logits based on the counts."""
        self.vocab_logits = self._normalize(m_vocab)
        self.rules_logits = self._normalize(m_rules)
        
    def update_tied_langs(self, langs: List[str], vocab_langs: List[int]):
        """
        Update the tying of vocab and rules by language.
        
        Args:
            langs: The languages.
            vocab_langs: The vocabulary languages.
        """
        assert len(vocab_langs) == len(self.vocab), "vocab_langs must have the same length as vocab"
        rules_langs = get_rules_bitmask(langs, self.rules)

        self.langs = list(langs)
        if len(langs) <= 256:
            # select bit width based on number of languages
            dtype = (np.uint8 if len(langs) <= 8 else
                     np.uint16 if len(langs) <= 16 else
                     np.uint32 if len(langs) <= 32 else
                     np.uint64 if len(langs) <= 64 else
                     np.uint128 if len(langs) <= 128 else
                     np.uint256)
            self.vocab_langs = np.array(vocab_langs, dtype=dtype)
            self.rules_langs = np.array(rules_langs, dtype=dtype)
        else:
            self.vocab_langs = list(vocab_langs)
            self.rules_langs = rules_langs
        
        if self.morpher is not None:
            # re-create morpher
            self.morpher = Morpher(self.langs, self.vocab, self.rules, 
                                   min_base_length=self.morpher.min_base_length,
                                   vocab_langs=self.vocab_langs, rules_langs=self.rules_langs)
        
    def encode(self, word: str, langs: Optional[Union[str,List[str]]] = None, 
               force_slow: bool = False, eow_applied: bool = False) -> List[Tuple[int, int]]:
        """
        Encode a word into pairs of vocab and rule ids.
        
        Args: 
            word: The word to encode.
            langs: The languages to use (should only be supplied during training!).
            force_slow: Whether to force slow decomposition.
            eow_applied: Whether the end-of-word token has already been applied.
            
        Returns:
            The list of vocab and rule ids.
        """
        if not eow_applied:
            if word.endswith(SHY):
                word = word[:-1]
            else:
                word = word + EOW
        lattice = self.build_lattice(word, langs, force_slow=force_slow)
        path = lattice.viterbi() # [(i, j, logit, data), ...]
        if path is None:
            return [(self.unk_token_id, 0)]
        return [data for _, _, _, data in path]
    
    def decode(self, ids: List[Tuple[int, int]], append_shy: bool = False) -> str:
        """
        Decode a list of vocab and rule ids into a word.
        
        Args:
            tokens: The list of vocab and rule ids.
            append_shy: Whether to append a soft hyphen.
        
        Returns:
            The decoded word.
        """
        word = "".join(self.morpher.compose(ids))
        if word.endswith(EOW):
            word = word[:-1]
        elif append_shy:
           word = word + SHY
        return word
    
    def add_marginal(self, word, count, langs, m_vocab, m_rules, force_slow=False):
        """
        Add the marginal counts for a word.
        
        Args:
            word: The word.
            count: The count.
            langs: The languages.
            m_vocab: The vocabulary counts.
            m_rules: The rules counts.
            force_slow: Whether to force slow decomposition.
        """
        lattice = self.build_lattice(word, langs, force_slow=force_slow)
        lattice.forward_sum()
        lattice.backward_sum()
        logits = lattice.marginal_logits()
        for l, e in zip(logits, lattice.edges):
            if not np.isfinite(l):
                continue
            vocab_id, rule_id = e[-1]
            l = np.exp(l) * count
            m_vocab[vocab_id] += l
            m_rules[rule_id] += l
        assert np.isfinite(lattice.logits_forward[-1])
        return lattice.logits_forward[-1] * count
    
    def add_vocab_loss(self, word, count, langs, losses, force_slow=False):
        """
        Add the removal losses for a word.
        
        Args:
            word: The word.
            count: The count.
            langs: The languages.
            losses: The losses.
            force_slow: Whether to force slow decomposition.
        """
        lattice = self.build_lattice(word, langs, force_slow=force_slow)
        lattice.forward_sum()
        lattice.backward_sum()
        removal_losses = lattice.removal_losses()
        for l, e in zip(removal_losses, lattice.edges):
            if not np.isfinite(l):
                continue
            vocab_id = e[-1][0] # (start, end, logit, (vocab_id, rule_id))
            losses[vocab_id] += l * count

    def build_lattice(self, word, langs, force_slow=False):
        """
        Build a lattice for a word.
        
        Args:
            word: The word.
            langs: The languages.
            force_slow: Whether to force slow decomposition.
            
        Returns:
            The lattice.
        """
        lattice = Lattice(len(word)+1)
        for vocab_id, rule_id, i, j in self.morpher.decompose(word, langs, force_slow=force_slow):
            logit = (float(self.vocab_logits[vocab_id]) * self.alpha +
                     float(self.rules_logits[rule_id]) * self.beta)
            penalty = self.rules[rule_id].penalty
            lattice.add_edge(i, j, logit - penalty - i * SHIFT, (vocab_id, rule_id))
        return lattice
    
    def rearrange_vocab(self, order):
        """
        Rearrange the vocabulary.
        
        Args:
            order: The new order.
        """
        self.vocab = [self.vocab[i] for i in order]
        self.vocab_lookup = {v: i for i, v in enumerate(self.vocab)}
        self.vocab_logits = self.vocab_logits[order]
        if self.vocab_langs is not None:
            self.vocab_langs = self.vocab_langs[order]
        if self.morpher is not None:
            # re-create morpher
            self.morpher = Morpher(self.langs, self.vocab, self.rules, 
                                   min_base_length=self.morpher.min_base_length,
                                   vocab_langs=self.vocab_langs, rules_langs=self.rules_langs)

    def format_token(self, tid: int, rid: int) -> str:
        """
        Format a token into human readable markup.
        
        Args:
            tid: The vocab id.
            rid: The rule id.
            
        Returns:
            The formatted token.
        """
        return format([(tid, rid)], self.morpher)

    def thumbprint(self) -> str:
        """Return a thumbprint of the model."""
        key = f"{(self.alpha, self.beta, self.min_base_len, self.vocab, self.rules)}"
        md5 = hashlib.md5(key.encode("utf-8")).digest()
        return b64encode(md5[:6]).decode("utf-8")
    
    def save_dict(self) -> dict:
        return {
            'langs': list(self.langs),
            'vocab': list(self.vocab),
            'rules': [r.save_dict() for r in self.rules],
            'alpha': self.alpha,
            'beta': self.beta,
            'unk_token_id': self.unk_token_id,
            'min_base_len': self.min_base_len,
            'vocab_logits': self.vocab_logits.tolist(),
            'vocab_langs': self.vocab_langs.tolist() if self.vocab_langs is not None else None,
            'rules_logits': self.rules_logits.tolist()
        }
    
    @staticmethod
    def load_dict(data: dict):
        return Model(vocab=data['vocab'],
                     rules=[MorphRule.load_dict(r) for r in data['rules']],
                     alpha=data['alpha'],
                     beta=data['beta'],
                     unk_token_id=data['unk_token_id'],
                     min_base_len=data['min_base_len'],
                     vocab_logits=data['vocab_logits'],
                     rules_logits=data['rules_logits'],
                     langs=data.get('langs'),
                     vocab_langs=data.get('vocab_langs'))
