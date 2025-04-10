# Path: umtoken/langs/fr.py

from umtoken.rules import RegexOp
from umtoken.langs.utils import DEFAULT_RULES, suffix_rules, interfix_rules

_lang = 'fr'

FR_RULES = (DEFAULT_RULES + 
            suffix_rules(_lang, ['e','ea','eai','eaient','eais','eait','eant','eante','eantes','eants','eas','ement','ent','eons','er','es','ez','eâmes','eâtes'], constraint_regex='[^e]$') +
            suffix_rules(_lang, ['s'], constraint_regex='([^es]|ee)$') +
            suffix_rules(_lang, ['a','ai','aient','ais','ait','ant','ante','antes','ants','as','i','ie','ies','iez','ir','irent','is','issaient','issais','issait','issant','issante','issantes','issants','issent','issez','issiez','issions','issons','it','ment','ons','re','u','ue','ues','us','âmes','âtes','èrent','é','ée','ées','és','îmes','îtes']) +
            suffix_rules(_lang, ['aux'], op=RegexOp(r'al$', r'', r'$', r'al')) +
            suffix_rules(_lang, ['','s'], op=RegexOp(r'([st])iv$', r'\1if', r'([st])if$', r'\1iv')) +
            suffix_rules(_lang, ['a','ai','aient','ais','ait','ant','ante','antes','ants','as','ons','âmes','âtes'], op=RegexOp(r'c$', r'ç', r'ç$', r'c')) +
            [])
