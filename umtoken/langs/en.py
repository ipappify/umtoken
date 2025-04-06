# Path: umtoken/langs/en.py

from umtoken.rules import RegexOp
from umtoken.langs.utils import DEFAULT_RULES, suffix_rules, interfix_rules

_lang = 'en'

EN_RULES = (DEFAULT_RULES + 
            suffix_rules(_lang, ['e','ed','ely','er','ers','es','est'], constraint_regex='[^e]$') +
            suffix_rules(_lang, ['s'], constraint_regex='([^es]|ee)$') +
            suffix_rules(_lang, ['able','ables','ably','ible','ibly','ing','ings','ly']) +
            suffix_rules(_lang, ['ed','er','ers','es'], op=RegexOp(r'y$', r'i', r'i$', r'y')) +
            suffix_rules(_lang, ['able','ables','ably','er','ers','ing','ings'], op=RegexOp(r'([bdfgklmnprst])$', r'\1\1', r'([bdfgklmnprst])\1$', r'\1')) +
            [])
