# Path: umtoken/langs/sv.py

from umtoken.rules import RegexOp
from umtoken.langs.utils import DEFAULT_RULES, suffix_rules, interfix_rules

_lang = 'sv'

SV_RULES = (DEFAULT_RULES + 
            suffix_rules(_lang, ['e','else','elsen','elser','elserna','en','ende','ens','er','erna','ernas','ers','es','et','ets'], constraint_regex='[^e]$') +
            suffix_rules(_lang, ['s'], constraint_regex='([^es]|ee)$') +
            suffix_rules(_lang, ['a','ad','ade','ades','an','ande','ans','ar','are','arna','arnas','ars','as','ast','aste','at','ats','bar','bara','bart','d','da','dd','dda','dde','ddes','de','des','het','heten','heter','heterna','it','its','ligen','n','na','nas','ning','ningar','ningarna','ningen','ns','or','orna','ornas','ors','r','rna','rnas','rs','t','ta','te','tes','ts','tt','tts']) +
            interfix_rules(_lang, ['s'], constraint_regex='([^es]|ee)$') +
            [])
