# Path: umtoken/langs/de.py

from umtoken.rules import RegexOp
from umtoken.langs.utils import DEFAULT_RULES, suffix_rules, interfix_rules

_lang = 'de'

DE_RULES = (DEFAULT_RULES + 
            suffix_rules(_lang, ['e','em','en','ene','enem','enen','ener','enes','ens','er','ern','es'], constraint_regex='[^e]$') +
            suffix_rules(_lang, ['s'], constraint_regex='([^es]|ee)$') +
            suffix_rules(_lang, ['nen'], constraint_regex='in$') +
            suffix_rules(_lang, ['e','en','st','t','te','tem','ten','ter','tes','tet'], constraint_regex='([bfghklmnprsxzß]|au|eu|ei)$') +
            suffix_rules(_lang, ['e','en','est','et','ete','etem','eten','eter','etes','etet'], constraint_regex='([dt]|[bdfhkg][mn])$') +
            suffix_rules(_lang, ['n'], constraint_regex='e[lr]$') +
            suffix_rules(_lang, ['en','ene','enem','enen','ener','enes','et','ete','etem','eten','eter','etes','t','te','tem','ten','ter','tes'], op=RegexOp(r'^', r'ge', r'^ge', r'')) +
            suffix_rules(_lang, ['ung','ungen'], constraint_regex='[^ea]$') +
            interfix_rules(_lang, ['e','en','ens','er','es'], constraint_regex='[^e]$') +
            interfix_rules(_lang, ['s'], constraint_regex='([^es]|ee)$') +
            interfix_rules(_lang, ['ungs'], constraint_regex='[^ea]$') +
            [])
