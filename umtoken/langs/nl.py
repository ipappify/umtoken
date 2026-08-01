# Path: umtoken/langs/nl.py

from umtoken.rules import RegexOp
from umtoken.langs.utils import DEFAULT_RULES, suffix_rules, interfix_rules

_lang = 'nl'

NL_RULES = (DEFAULT_RULES + 
            suffix_rules(_lang, ['e','en','ene','ens','er','ere','eren','ers','es','etje','etjes'], constraint_regex='[^e]$') +
            suffix_rules(_lang, ['s','st','ste'], constraint_regex='([^es]|ee)$') +
            suffix_rules(_lang, ['baar','bare','d','de','den','heden','heid','ing','ingen','je','jes','pje','pjes','t','te','ten','tje','tjes','ën']) +
            suffix_rules(_lang, ['d','de','den','t'], op=RegexOp(r'([aeou])([bcdfgklmnprst])$', r'\1\1\2', r'([aeou])\1([bcdfgklmnprst])$', r'\1\2')) +
            suffix_rules(_lang, ['d','de','en','ene','ens','t','te'], op=RegexOp(r'^', r'ge', r'^ge', r'')) +
            interfix_rules(_lang, ['e','en','er','eren'], constraint_regex='[^e]$') +
            interfix_rules(_lang, ['s'], constraint_regex='([^es]|ee)$') +
            interfix_rules(_lang, ['ën']) +
            [])
