# Path: umtoken/langs/es.py

from umtoken.rules import RegexOp
from umtoken.langs.utils import DEFAULT_RULES, suffix_rules, interfix_rules

_lang = 'es'

ES_RULES = (DEFAULT_RULES + 
            suffix_rules(_lang, ['e','emente','emos','en','er','es'], constraint_regex='[^e]$') +
            suffix_rules(_lang, ['a','aba','abais','aban','abas','ada','adas','ado','ados','amente','amos','an','ando','ante','antes','ar','aron','as','aste','asteis','ida','idas','ido','idos','iendo','iente','ientes','ieron','imos','ir','iste','isteis','ió','mente','o','os','ábamos','áis','ás','é','éis','és','í','ía','íais','íamos','ían','ías','ís','ó']) +
            suffix_rules(_lang, ['es'], op=RegexOp(r'z$', r'c', r'c$', r'z')) +
            [])
