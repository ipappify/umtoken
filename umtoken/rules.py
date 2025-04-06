# Path: umtoken/rules.py

from typing import Dict, List, Optional, Tuple, Union, Iterable
import regex as re

from .alphabet import ASCII_RESERVED_EOW as EOW

class MorphOp:
    def __init__(self):
        """Abstract base class for morphological operation."""

    def apply(self, base: str) -> str:
        """Transform base to stem.
        Args: 
            base: base to transform.
        Returns:
            The stem."""
        raise NotImplementedError("Cannot call abstract method. Concrete class must implement apply method.")
    
    def can_apply(self, base: str) -> bool:
        """Check if op can be applied to base.
        Args: 
            base: base to check.
        Returns:
            True if op can be applied to base."""
        raise NotImplementedError("Cannot call abstract method. Concrete class must implement can_apply method.")
    
    def revert(self, stem: str) -> str:
        """Transform stem to base.
        Args:
            stem: stem to transform.
        Returns:
            The base."""
        raise NotImplementedError("Cannot call abstract method. Concrete class must implement revert method.")
    
    def can_revert(self, stem: str) -> bool:
        """Check if op can revert stem to base. Check may only return true if revert+apply is unambiguous.
        Args:
            stem: stem to check.
        Returns:
            True if op can revert stem to base."""
        raise NotImplementedError("Cannot call abstract method. Concrete class must implement can_revert method.")
    
    def is_same(self, other) -> bool:
        """Check if two ops are the same.
        Args:
            other: Other op to compare.
        Returns:
            True if ops are the same."""
        raise NotImplementedError("Cannot call abstract method. Concrete class must implement is_same method.")
    
    def is_unconditional(self) -> bool:
        """Check if op is unconditional. Unconditional ops can be applied to any base.
        Returns:
            True if op is unconditional."""
        raise NotImplementedError("Cannot call abstract method. Concrete class must implement is_unconditional method.")

    def save_dict(self) -> dict:
        """Save op to dict.
        Returns:
            The dict."""
        raise NotImplementedError("Cannot call abstract method. Concrete class must implement save_dict method.")

    @staticmethod
    def load_dict(data: Optional[Dict]):
        """Load op from dict.
        Args:
            data: The dict.
        Returns:
            The op."""
        if data is None:
            return None
        if not 'type' in data:
            raise ValueError("Missing type in MorphOp dict")
        if data['type'] == 'regex':
            return RegexOp.load_dict(data)
        else:
            raise ValueError(f"Unknown MorphOp type: {data['type']}")


class RegexOp(MorphOp):
    def __init__(self, apply_regex, apply_sub, revert_regex, revert_sub):
        """
        Applies regex substitution to base.
        
        Args:
            apply_regex: regex pattern to apply to base
            apply_sub: replacement for apply_regex
            revert_regex: regex pattern to revert to base
            revert_sub: replacement for revert_regex
        """
        super().__init__()
        self.apply_regex = re.compile(apply_regex)
        self.apply_sub = apply_sub
        self.revert_regex = re.compile(revert_regex)
        self.revert_sub = revert_sub

    def apply(self, base: str) -> str:
        return self.apply_regex.sub(self.apply_sub, base)
    
    def can_apply(self, base: str) -> bool:
        return self.apply_regex.search(base) is not None
    
    def revert(self, stem: str) -> str:
        return self.revert_regex.sub(self.revert_sub, stem)
    
    def can_revert(self, stem: str) -> bool:
        return self.revert_regex.search(stem) is not None
    
    def is_same(self, other) -> bool:
        return (isinstance(other, RegexOp) and
                self.apply_regex.pattern == other.apply_regex.pattern and
                self.apply_sub == other.apply_sub and
                self.revert_regex.pattern == other.revert_regex.pattern and
                self.revert_sub == other.revert_sub)
        
    def is_unconditional(self) -> bool:
        return all(c in '^$.+*?' for c in self.apply_regex.pattern)
    
    def __str__(self) -> str:
        return f"re('{self.apply_regex.pattern}','{self.apply_sub}')"
    
    def __repr__(self):
        return self.__str__()
    
    def save_dict(self) -> dict:
        return {
            'type': 'regex',
            'apply_regex': self.apply_regex.pattern,
            'apply_sub': self.apply_sub,
            'revert_regex': self.revert_regex.pattern,
            'revert_sub': self.revert_sub
        }
    
    @staticmethod
    def load_dict(data: Dict):
        return RegexOp(apply_regex=data['apply_regex'], 
                       apply_sub=data['apply_sub'], 
                       revert_regex=data['revert_regex'], 
                       revert_sub=data['revert_sub'])


class MorphRule():
    def __init__(self, 
                 langs: Optional[Union[str, list[str]]], 
                 op: Optional[MorphOp] = None,
                 constraint_regex: Optional[str] = None, 
                 penalty: Optional[float] = 0.0,
                 min_base_length: Optional[int] = None,):
        """
        Abstract base class for morphological rule.

        Args:
            langs: Language or list of languages to which rule applies. None: all languages.
            op: Morphological operation.
            constraint_regex: Regex pattern for constraint. The rule will only be applied to bases that match the constraint.
            penalty: Penalty for applying this rule.
            min_base_length: Minimum length of base for rule to apply.
        """
        self.op = op
        self.constraint_regex = re.compile(constraint_regex) if constraint_regex else None
        self.penalty = penalty or 0.0
        self.min_base_length = min_base_length
        self._set_langs(langs)

    def _set_langs(self, langs: Optional[Union[str, list[str]]]):
        if not langs or any(i is None for i in langs):
            self.langs = None
            self.any_lang = True
        else:
            self.langs = [langs] if isinstance(langs, str) else list(sorted(set(langs)))
            self.any_lang = False

    def apply(self, base: str):
        """Transform base to word.
        Args:
            base: base to transform.
        Returns:
            The word."""
        raise NotImplementedError("Cannot call abstract method. Concrete class must implement apply method.")
    
    def can_apply(self, base: str):
        """Check if rule can be applied to base. Constraints are not checked here.
        Args:
            base: base to check.
        Returns:
            True if rule can be applied to base."""
        raise NotImplementedError("Cannot call abstract method. Concrete class must implement can_apply method.")
    
    def revert(self, word: str):
        """Transform word towards stem.
        Args:
            word: Word to transform.
        Returns:
            The stem."""
        raise NotImplementedError("Cannot call abstract method. Concrete class must implement can_apply method.")
    
    def can_revert(self, word: str):
        """Check if rule can be reverted from word. Constraints are not checked here.
        Args:
            word: Word to check.
        Returns:
            True if rule can be reverted from word."""
        raise NotImplementedError("Cannot call abstract method. Concrete class must implement can_apply method.")
    
    def is_same(self, other):
        """Check if rule is the same as other rule. Constraints and penalties are not checked.
        Args:
            other: Other rule to compare.
        Returns:
            True if rules are the same."""
        raise NotImplementedError("Cannot call abstract method. Concrete class must implement can_apply method.")
    
    def has_any_lang(self, langs: list[Optional[str]]):
        """Check if rule has any language.
        Args:
            langs: Languages to check.
        Returns:
            True if rule has any language."""
        if self.any_lang:
            return True
        if not langs:
            return True
        if isinstance(langs, str):
            return langs in self.langs
        if any(not lang for lang in langs):
            return True
        return any(lang in self.langs for lang in langs)

    def save_dict(self) -> dict:
        """Save rule to dict.
        Returns:
            The dict."""
        raise NotImplementedError("Cannot call abstract method. Concrete class must implement save_dict method.")
    
    @staticmethod
    def load_dict(data: Dict):
        """Load rule from dict.
        Args:
            data: The dict.
        Returns:
            The rule."""
        if not 'type' in data:
            raise ValueError("Missing type in MorphRule dict")
        if data['type'] == 'suffix':
            return SuffixRule.load_dict(data)
        else:
            raise ValueError(f"Unknown MorphRule type: {data['type']}")
        
    @staticmethod
    def merge_duplicates(rules: List) -> List:
        """Merge duplicate rules.
        Args:
            rules: List of rules.
        Returns:
            List of merged rules."""
        result = []
        for r in rules:
            assert isinstance(r, MorphRule)
            existing: MorphRule = [r2 for r2 in result if r2.is_same(r)]
            if len(existing) == 0:
                # add a copy that we can modify
                result.append(MorphRule.load_dict(r.save_dict()))
            else:
                existing = existing[0]
                # merge langs
                existing._set_langs((existing.langs or [None]) + (r.langs or [None]))
                # merge constraints (use least restrictive)
                if existing.constraint_regex is None or r.constraint_regex is None:
                    existing.constraint_regex = None
                elif existing.constraint_regex.pattern != r.constraint_regex.pattern:
                    # merge with '|'
                    existing.constraint_regex = re.compile(f"({existing.constraint_regex.pattern}|{r.constraint_regex.pattern})")
                else:
                    pass
                # merge penalties (use smallest penalty)
                existing.penalty = min(existing.penalty, r.penalty)
        return result
    
    @staticmethod
    def sort(rules: List) -> List:
        """Sort rules by suffix/penalty. First two rules are empty rule and end of word rule.
        Args:
            rules: List of rules.
        Returns:
            List of sorted rules."""
            
        rule0 = [r for r in rules if isinstance(r, SuffixRule) and r.suffix == '' and r.op is None and r.constraint_regex is None]
        rule1 = [r for r in rules if isinstance(r, SuffixRule) and r.suffix == EOW and r.op is None and r.constraint_regex is None]
        
        assert len(rule0) == 1, "Need exactly one empty rule"
        assert len(rule1) == 1, "Need exactly one end of word rule"
        
        rule0 = rule0[0]
        rule1 = rule1[0]
        rules = [r for r in rules if r != rule0 and r != rule1]
        rules.sort(key=lambda r: r.suffix if isinstance(r, SuffixRule) else r.penalty)
            
        return [rule0, rule1] + rules
    
    def drop_constraint(self):
        """Drop constraints from this rule.
        Returns:
            A new rule without constraint."""
        if not self.constraint_regex:
            return self
        new_rule = MorphRule.load_dict(self.save_dict())
        new_rule.constraint_regex = None
        return new_rule
    
    def drop_penalty(self):
        """Drop penalty from this rule.
        Returns:
            A new rule without penalty."""
        if self.penalty == 0.0:
            return self
        new_rule = MorphRule.load_dict(self.save_dict())
        new_rule.penalty = 0.0
        return new_rule
    
    def add_penalty(self, bias: float):
        """Add bias to penalty of this rule.
        Args:
            bias: The bias to add.
        Returns:
            A new rule with added penalty."""
        new_rule = MorphRule.load_dict(self.save_dict())
        new_rule.penalty += bias
        return new_rule

        
class SuffixRule(MorphRule):
    def __init__(self, 
                 suffix: str,
                 langs: Optional[Union[str, list[str]]], 
                 op: Optional[MorphOp] = None,
                 constraint_regex: Optional[str] = None, 
                 penalty: Optional[float] = 0.0,
                 min_base_length: Optional[int] = None):
        """
        Suffix rule.

        Args:
            suffix: Suffix to append to base.
            langs: Language or list of languages to which rule applies. None: all languages.
            op: Morphological operation.
            constraint_regex: Regex pattern for constraint.
            penalty: Penalty for applying this rule.
            min_base_length: Minimum length of base for rule to apply.
        """
        super().__init__(langs, op, constraint_regex, penalty, min_base_length)
        self.suffix = suffix

    def apply(self, base: str):
        stem = self.op.apply(base) if self.op else base
        return stem + self.suffix
    
    def can_apply(self, base: str):
        return self.op.can_apply(base)
    
    def revert(self, word: str):
        stem = word[:-len(self.suffix)]
        return self.op.revert(stem) if self.op else stem
    
    def can_revert(self, word: str):
        if self.suffix == '' and word.endswith(EOW):
            return False
        if not (len(word) > len(self.suffix) and word.endswith(self.suffix)):
            return False
        if not self.op:
            return True
        stem = word[:-len(self.suffix)]
        return self.op.can_revert(stem)
    
    def is_same(self, other):
        return (isinstance(other, SuffixRule) and
                self.suffix == other.suffix and
                (self.op is None) == (other.op is None) and
                (self.op is None or self.op.is_same(other.op)))
    
    def __str__(self) -> str:
        return f"suffix(-{self.suffix},{self.op})"
    
    def __repr__(self):
        return self.__str__()
    
    def save_dict(self) -> dict:
        return {
            'type': 'suffix',
            'langs': list(self.langs) if self.langs else None,
            'suffix': self.suffix,
            'op': self.op.save_dict() if self.op else None,
            'constraint_regex': self.constraint_regex.pattern if self.constraint_regex else None,
            'penalty': self.penalty,
            'min_base_length': self.min_base_length
        }
    
    @staticmethod
    def load_dict(data: dict):
        return SuffixRule(langs=data.get('langs'), 
                          suffix=data['suffix'], 
                          op=MorphOp.load_dict(data.get('op')), 
                          constraint_regex=data.get('constraint_regex'), 
                          penalty=data.get('penalty',0.0), 
                          min_base_length=data.get('min_base_length'))
