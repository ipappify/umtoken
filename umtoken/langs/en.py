# Path: umtoken/langs/en.py

from umtoken.rules import RegexOp
from umtoken.langs.utils import DEFAULT_RULES, suffix_rules, interfix_rules

_lang = 'en'

EN_RULES = (DEFAULT_RULES + 
            suffix_rules(_lang, ['e','ed','ely','en','er','ers','es','est'], constraint_regex='[^e]$') +
            suffix_rules(_lang, ['s'], constraint_regex='([^es]|ee)$') +
            suffix_rules(_lang, ['able','ables','ably','ful','ible','ibly','ing','ings','ities','ity','ly','ment','ments','ness']) +
            suffix_rules(_lang, ['ed','er','ers','es','est','ly'], op=RegexOp(r'y$', r'i', r'i$', r'y')) +
            suffix_rules(_lang, ['able','ables','ably','ed','en','er','ers','est','ing','ings'], op=RegexOp(r'([bdfgklmnprst])$', r'\1\1', r'([bdfgklmnprst])\1$', r'\1')) +
            [])
