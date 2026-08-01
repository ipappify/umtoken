# Path: umtoken/langs/es.py

from umtoken.rules import RegexOp
from umtoken.langs.utils import DEFAULT_RULES, suffix_rules, interfix_rules

_lang = 'es'

ES_RULES = (DEFAULT_RULES + 
            suffix_rules(_lang, ['e','edor','edora','edoras','edores','emente','emos','en','er','eremos','erá','erán','erás','eré','eréis','ería','eríais','eríamos','erían','erías','es'], constraint_regex='[^e]$') +
            suffix_rules(_lang, ['a','aba','abais','aban','abas','able','ables','aciones','ación','ada','adas','ado','ador','adora','adoras','adores','ados','aje','ajes','amente','amos','an','ando','ante','antes','ar','ara','aran','aras','aremos','aron','ará','arán','arás','aré','aréis','aría','aríais','aríamos','arían','arías','as','aste','asteis','ible','ibles','ida','idad','idades','idas','ido','idos','iendo','iente','ientes','iera','ieran','ieras','ieron','imos','ir','iremos','irá','irán','irás','iré','iréis','iría','iríais','iríamos','irían','irías','iste','isteis','ió','mente','o','os','ábamos','áis','ás','é','éis','és','í','ía','íais','íamos','ían','ías','ís','ó']) +
            suffix_rules(_lang, ['es'], op=RegexOp(r'z$', r'c', r'c$', r'z')) +
            suffix_rules(_lang, ['e','emos','en','es','é','éis'], op=RegexOp(r'c$', r'qu', r'qu$', r'c')) +
            suffix_rules(_lang, ['e','emos','en','es','é','éis'], op=RegexOp(r'g$', r'gu', r'gu$', r'g')) +
            suffix_rules(_lang, ['e','emos','en','es','é','éis'], op=RegexOp(r'z$', r'c', r'c$', r'z')) +
            [])
