from typing import List
from warnings import warn

from ..rules import MorphRule
from .utils import DEFAULT_RULES
from .de import DE_RULES
from .el import EL_RULES
from .en import EN_RULES
from .es import ES_RULES
from .fr import FR_RULES
from .hu import HU_RULES
from .it import IT_RULES
from .nl import NL_RULES
from .pl import PL_RULES
from .pt import PT_RULES
from .ro import RO_RULES

RULES_BY_LANGS = {
    "de": DE_RULES,
    "el": EL_RULES,
    "en": EN_RULES,
    "es": ES_RULES,
    "fr": FR_RULES,
    "hu": HU_RULES,
    "it": IT_RULES,
    "nl": NL_RULES,
    "pl": PL_RULES,
    "pt": PT_RULES,
    "ro": RO_RULES,
}

def get_rules(languages: List[str], 
              drop_constraints: bool = False,
              drop_penalties: bool = False,
              remove_op_rules: bool = False,
              remove_unconditional_op_rules: bool = False,
              add_penalties: float = 0.0) -> List[MorphRule]:
    """
    Returns the rules for a list of languages.
    
    Args:
        languages: A list of languages.
        drop_constraints: Whether to drop constraints from rules (default: False).
        drop_penalties: Whether to drop penalties from rules (default: False).
        remove_op_rules: Whether to remove rules with morph ops (default: False).
        remove_unconditional_op_rules: Whether to remove rules with unconditional morph ops which are applicable to all bases (default: False).
        add_penalties: The bias to add to the penalties for non-default rules (default: 0.0).
        
    Returns:
        The rules for the languages
    """
        
    rules = DEFAULT_RULES
    for lang in languages:
        lang_rules = RULES_BY_LANGS.get(lang, None)
        if lang_rules is not None:
            rules += lang_rules
        else:
            warn(f"No rules defined for language {lang}.")
    if remove_op_rules:
        rules = [rule for rule in rules if not rule.op]
    elif remove_unconditional_op_rules:
        rules = [rule for rule in rules if not (rule.op and rule.op.is_unconditional())]
    if drop_constraints:
        rules = [rule.drop_constraint() for rule in rules]
    if drop_penalties:
        rules = [rule.drop_penalty() for rule in rules]
    rules = MorphRule.merge_duplicates(rules)
    rules = MorphRule.sort(rules)
    if add_penalties:
        rules = [rule.add_penalty(add_penalties) if i > 1 else rule for i, rule in enumerate(rules)]
    return rules
    