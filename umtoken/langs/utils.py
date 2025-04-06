# Path: umtoken/langs/utils.py

from typing import List, Optional

from ..rules import SuffixRule, MorphOp
from ..alphabet import ASCII_RESERVED_EOW as EOW

SMALL_PENALTY = 0.75
LARGE_PENALTY = 1.5

DEFAULT_RULES = [
    SuffixRule('', None),
    SuffixRule(EOW, None),
]

def suffix_rules(lang: str, suffixes: List[str], op: Optional[MorphOp] = None, 
                 constraint_regex: Optional[str] = None, penalty: float = 0.0,
                 min_base_length: Optional[int] = None) -> List[SuffixRule]:
    """
    Create a list of suffix rules (word ends).

    Args:
        lang: The language of the suffixes.
        suffixes: The suffixes. EOW is added to the end of each suffix if it is not already there.
        op: The operation to apply.
        constraint_regex: The constraint regex.
        penalty: The penalty.
        min_base_length: The minimum base length for applying the suffix rule.
    
    Returns:
        The list of suffix rules.
    """

    suffixes = [s + (EOW if not s.endswith(EOW) else "") for s in suffixes]
    return [SuffixRule(suffix=s, langs=lang, op=op, constraint_regex=constraint_regex, 
                       penalty=penalty, min_base_length=min_base_length) for s in suffixes]

def interfix_rules(lang: str, interfixes: List[str], op: Optional[MorphOp] = None, 
                   constraint_regex: Optional[str] = None, penalty: float = SMALL_PENALTY,
                   min_base_length: Optional[int] = None) -> List[SuffixRule]:
    """
    Create a list of interfix rules (word contains).

    Args:
        lang: The language of the interfixes.
        interfixes: The interfixes.
        op: The operation to apply.
        constraint_regex: The constraint regex.
        penalty: The penalty. Per default, a small penalty is applied.
        min_base_length: The minimum base length for applying the suffix rule.
    
    Returns:
        The list of interfix rules.
    """

    return [SuffixRule(suffix=i, langs=lang, op=op, constraint_regex=constraint_regex, 
                       penalty=penalty, min_base_length=min_base_length) for i in interfixes]
