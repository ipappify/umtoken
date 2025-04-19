# Path: umtoken/langs/sv.py

from umtoken.rules import RegexOp
from umtoken.langs.utils import DEFAULT_RULES, suffix_rules, interfix_rules

_lang = 'sv'

SV_RULES = (DEFAULT_RULES + 
            suffix_rules(_lang, ['en','ende','ens','er','erna','ernas','ers','es','et','ets'], constraint_regex='[^e]$') +
            suffix_rules(_lang, ['s'], constraint_regex='([^es]|ee)$') +
            suffix_rules(_lang, ['a','ad','ade','ades','an','ande','ans','ar','arna','arnas','ars','as','at','ats','d','dd','dde','ddes','de','des','it','its','ligen','n','na','nas','ns','or','orna','ornas','ors','r','rna','rnas','rs','t','te','tes','ts','tt','tts']) +
            [])
