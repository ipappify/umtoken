# Path: umtoken/morpher.py

from typing import List, Optional, Union, Iterable, Tuple

from .alphabet import ASCII_RESERVED_EOW as EOW
from .trie import DictTrie, LookupTrie
from .rules import MorphRule, SuffixRule
from .utils import get_rules_bitmask, get_langs_bitmask

class Morpher:
    def __init__(self,
                 langs: list[str],
                 vocab: list[str], 
                 rules: list[MorphRule],
                 vocab_langs: Optional[list[int]] = None,
                 rules_langs: Optional[list[int]] = None,
                 min_base_length: int = 2,
                 prebuild_stem_trie: bool = False) -> None:
        """
        Decompose words into bases and rules.

        Args:
            vocab: List of bases.
            rules: List of morphological rules.
            min_base_length: Minimum length of bases to which rules may be applied.
            prebuild_stem_trie: Whether to prebuild the stem trie for faster decomposition.
                                If False, the stem trie is built on the first call to decompose_fast.
                                decompose_slow does not use the stem trie and does not build it.
        """

        assert len(rules) >= 2, f"need at least the two default rules (empty rule, end of word rule)"
        assert isinstance(rules[0], SuffixRule) and isinstance(rules[1], SuffixRule), f"first two rules must be SuffixRule instances"
        assert rules[0].suffix == "" and rules[0].op is None and rules[1].constraint_regex is None, f"first rule must be default empty rule"
        assert rules[1].suffix == EOW and rules[0].op is None and rules[1].constraint_regex is None, f"second rule must be default end of word rule"
        assert vocab_langs is None or len(vocab_langs) == len(vocab), f"vocab_langs must have the same length as vocab"
        assert rules_langs is None or len(rules_langs) == len(rules), f"rules_langs must have the same length as rules"

        self.langs = langs
        self.vocab = vocab # = bases
        self.rules = rules
        self.vocab_langs = vocab_langs
        self.rules_langs = rules_langs if rules_langs is not None else get_rules_bitmask(langs, rules)
        
        self.any_op = any(r.op for r in rules)
        self.min_base_length = min_base_length

        self.base_trie = DictTrie(pairs=[(l, i) for i, l in enumerate(self.vocab)])
        self.suffix_trie = LookupTrie(pairs=[(r.suffix, i) for i, r in enumerate(self.rules)])
        self.reverse_suffix_trie = LookupTrie(pairs=[(r.suffix[::-1], i) for i, r in enumerate(self.rules)])

        self.max_part_length = max(max(len(r.suffix) for r in self.rules if isinstance(r, SuffixRule)),
                                   max(len(l) for l in self.vocab))

        self.stem_trie = None
        if prebuild_stem_trie:
            self._build_stem_trie()

    def _build_stem_trie(self):
        if self.any_op and self.stem_trie is None:
            # TODO: it would be faster to group rules by ops so that each op is only applied once to each base
            stems = set()
            for j, r in enumerate(self.rules):
                if r.op is None:
                    continue
                for i, l in enumerate(self.vocab):
                    if len(l) < (r.min_base_length or self.min_base_length):
                        continue
                    if self.vocab_langs is not None and self.vocab_langs[i] & self.rules_langs[j] == 0:
                        continue
                    if r.op.can_apply(l):
                        stem = r.op.apply(l)
                        assert r.op.can_revert(stem), f"op {r.op} cannot be reverted for base {l} -> {stem}"
                        stems.add((stem, (i, j)))
            
            self.stem_trie = LookupTrie(pairs=stems) if len(stems) > 0 else None
            self.max_part_length = max(self.max_part_length, max(len(r) for r, _ in stems))
            
    def decompose(self, word: str, langs: Optional[Union[str,int,List[str]]], force_slow: bool = False) -> Iterable[Tuple[int, int, int, int]]:
        """Return all valid decompositions inside word as tuples (base index, rule index, start index, end index).
        Args:
            word: Word to decompose.
            lang: Language of word.
            force_slow: Whether to force slow decomposition (and prevent building the stem trie).
        Returns:
            Iterable of tuples (base index, rule index, start index, end index)."""
        
        lang_mask = get_langs_bitmask(self.langs, langs)            
        if force_slow:
            return self.decompose_slow(word, lang_mask)
        else:
            return self.decompose_fast(word, lang_mask)

    def decompose_single(self, part: str, lang_mask: Optional[int]) -> Iterable[Tuple[int, int]]:
        """Decompose the word part into tuples of base index and rule index.
        Args:
            part: Word part to decompose.
            lang_mask: Bitmask for language(s) of word.
        Returns:
            Iterable of tuples (base index, rule index)."""
        eow = part.endswith(EOW)
        for s, idxs in self.reverse_suffix_trie.prefixes_and_values(part[::-1]):
            if eow and not s.startswith(EOW): # EOW is reversed
                continue
            stem = part[:len(part)-len(s)]
            for i in idxs:
                rule = self.rules[i] # type: MorphRule
                # check langs
                if lang_mask is not None and i > 1 and self.rules_langs[i] & lang_mask == 0:
                    continue
                if rule.op is None or rule.op.can_revert(stem):
                    base = rule.op.revert(stem) if rule.op else stem
                    # bases of length smaller than min length 
                    # are only allowed for the default rules 0 and 1
                    if len(base) < (rule.min_base_length or self.min_base_length) and i >= 2: 
                        continue
                    # check base
                    if not base in self.base_trie:
                        continue
                    base_idx = self.base_trie[base]
                    # check constraint
                    if rule.constraint_regex and not rule.constraint_regex.search(base):
                        continue
                    # check vocab lang if available
                    if self.vocab_langs is not None:
                        if lang_mask is not None and self.vocab_langs[base_idx] & lang_mask == 0:
                            continue                        
                        if i > 1 and self.vocab_langs[base_idx] & self.rules_langs[i] == 0:
                            continue
                    
                    yield (base_idx, i)
        
    def decompose_slow(self, word: str, lang_mask: Optional[int]) -> Iterable[Tuple[int, int, int, int]]:
        """Return all valid decompositions inside word as tuples (base index, rule index, start index, end index).
        Does not require a stem trie.
        Args:
            word: Word to decompose.
            lang_mask: Bitmask for language(s) of word.
        Returns:
            Iterable of tuples (base index, rule index, start index, end index)."""
        for i in range(len(word)):
            for j in range(i + 1, len(word) + 1):
                part = word[i:j]
                for base_idx, rule_idx in self.decompose_single(part, lang_mask):
                    yield (base_idx, rule_idx, i, j)

    def decompose_fast(self, word: str, lang_mask: Optional[int]) -> Iterable[Tuple[int, int, int, int]]:
        """Return all valid decompositions inside word as tuples (base index, rule index, start index, end index).
        Requires a stem trie and builds it if not available.
        Args:
            word: Word to decompose.
            lang_mask: Bitmask for language(s) of word.
        Returns:
            Iterable of tuples (base index, rule index, start index, end index)."""
        # ensure that the stem trie is built
        self._build_stem_trie()

        stems = [[] for _ in range(len(word))]
        rules = [[('', 0)] for _ in range(len(word)+1)] # add empty rule

        # collect stems and rules for all parts
        for i in range(len(word)):
            part = word[i:i+self.max_part_length]

            # iterate over suffixes
            if i > 0:
                for suffix, rule_idxs in self.suffix_trie.prefixes_and_values(part):
                    for rule_idx in rule_idxs:
                        if rule_idx == 0: # empty rule is already added
                            continue
                        if lang_mask is not None and rule_idx > 1 and self.rules_langs[rule_idx] & lang_mask == 0:
                            continue
                        rules[i].append((suffix, rule_idx))

            # iterate over stems (= bases, for rules without op)
            for stem, base_idx in self.base_trie.prefixes_and_values(part):
                stems[i].append((stem, base_idx, None))

            # iterate over stems (= morphed bases)
            if not self.stem_trie is None:
                for stem, idxs in self.stem_trie.prefixes_and_values(word[i:]):
                    for base_idx, rule_idx in idxs:
                        stems[i].append((stem, base_idx, rule_idx))
        
        # combine stems and rules
        for i in range(len(word)):
            for stem, base_idx, allowed_rule_idx in stems[i]:
                base = self.vocab[base_idx]
                j = i + len(stem)
                for suffix, rule_idx in rules[j]:
                    if not (allowed_rule_idx is None or allowed_rule_idx == rule_idx):
                        continue
                    
                    rule = self.rules[rule_idx]
                    # only default rules 0 and 1 are allowed for bases of length smaller than min length
                    if len(base) < (rule.min_base_length or self.min_base_length) and rule_idx >= 2: 
                        continue

                    if allowed_rule_idx is None and rule.op:
                        continue

                    # this is already checked when building the stem trie
                    # assert rule.op.can_revert(stem), f"op {rule.op} cannot be reverted for base {base} -> {stem}"

                    k = j + len(suffix)
                    part = stem + suffix
                    if rule.constraint_regex and not rule.constraint_regex.search(base):
                        continue
                    
                    # check vocab lang if available
                    if self.vocab_langs is not None:
                        if lang_mask is not None and self.vocab_langs[base_idx] & lang_mask == 0:
                            continue
                        if rule_idx > 1 and self.vocab_langs[base_idx] & self.rules_langs[rule_idx] == 0:
                            continue

                    yield (base_idx, rule_idx, i, k)

    def compose(self, ids: Iterable[Tuple[int, int]]) -> Iterable[str]:
        """Compose bases and rules into words.
        Args:
            ids: Iterable of tuples (base index, rule index).
        Returns:
            Iterable of words."""
        for base_idx, rule_idx in ids:
            base = self.vocab[base_idx]
            rule = self.rules[rule_idx]
            yield rule.apply(base)
