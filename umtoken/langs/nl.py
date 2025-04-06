# Path: umtoken/langs/nl.py

from umtoken.rules import RegexOp
from umtoken.langs.utils import DEFAULT_RULES, suffix_rules, interfix_rules

_lang = 'nl'

NL_RULES = (DEFAULT_RULES + 
            suffix_rules(_lang, ['e','en','ene','ens','eren','es'], constraint_regex='[^e]$') +
            suffix_rules(_lang, ['s'], constraint_regex='([^es]|ee)$') +
            suffix_rules(_lang, ['d','de','den','ds','t','te','ten','ts','ën']) +
            suffix_rules(_lang, ['d','de','ds','en','ene','ens','t','te','ts'], op=RegexOp(r'^', r'ge', r'^ge', r'')) +
            interfix_rules(_lang, ['e','en','er','eren'], constraint_regex='[^e]$') +
            interfix_rules(_lang, ['s'], constraint_regex='([^es]|ee)$') +
            interfix_rules(_lang, ['ën']) +
            [])
