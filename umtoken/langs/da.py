# Path: umtoken/langs/da.py

from umtoken.rules import RegexOp
from umtoken.langs.utils import DEFAULT_RULES, suffix_rules, interfix_rules

_lang = 'da'

DA_RULES = (DEFAULT_RULES + 
            suffix_rules(_lang, ['e','ede','edes','en','ende','ene','enes','ens','er','erne','ernes','ers','es','et','ets'], constraint_regex='[^e]$') +
            suffix_rules(_lang, ['s'], constraint_regex='([^es]|ee)$') +
            suffix_rules(_lang, ['t','te','tes']) +
            suffix_rules(_lang, ['e','ede','edes','en','ende','er','es'], op=RegexOp(r'([bdfgklmnprst])$', r'\1\1', r'([bdfgklmnprst])\1$', r'\1')) +
            [])
