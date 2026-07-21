# Path: umtoken/langs/da.py

from umtoken.rules import RegexOp
from umtoken.langs.utils import DEFAULT_RULES, suffix_rules, interfix_rules

_lang = 'da'

DA_RULES = (DEFAULT_RULES + 
            suffix_rules(_lang, ['e','ede','edes','else','elsen','elser','elserne','en','ende','ene','enes','ens','er','ere','erne','ernes','ers','es','est','este','et','ets'], constraint_regex='[^e]$') +
            suffix_rules(_lang, ['s','st','ste'], constraint_regex='([^es]|ee)$') +
            suffix_rules(_lang, ['bar','bare','bart','hed','heden','heder','hederne','ning','ningen','ninger','ningerne','t','te','tes']) +
            suffix_rules(_lang, ['ne','nes'], constraint_regex='er$') +
            suffix_rules(_lang, ['r'], constraint_regex='[aeiouyæøå]$') +
            suffix_rules(_lang, ['e','ede','edes','en','ende','er','ere','es','est','este'], op=RegexOp(r'([bdfgklmnprst])$', r'\1\1', r'([bdfgklmnprst])\1$', r'\1')) +
            [])
