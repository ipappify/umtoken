# Path: umtoken/langs/fr.py

from umtoken.rules import RegexOp
from umtoken.langs.utils import DEFAULT_RULES, suffix_rules, interfix_rules

_lang = 'fr'

FR_RULES = (DEFAULT_RULES + 
            suffix_rules(_lang, ['e','eaient','eais','eait','eant','eante','eantes','eants','ement','ent','eons','er','es','ez'], constraint_regex='[^e]$') +
            suffix_rules(_lang, ['s'], constraint_regex='([^es]|ee)$') +
            suffix_rules(_lang, ['aient','ais','ait','ant','ante','antes','ants','i','ie','ies','iez','ir','is','issaient','issais','issait','issant','issante','issantes','issants','issent','issez','issiez','issions','issons','it','ment','ons','re','u','ue','ues','us','é','ée','ées','és']) +
            suffix_rules(_lang, ['aux'], op=RegexOp(r'al$', r'', r'$', r'al')) +
            suffix_rules(_lang, ['','s'], op=RegexOp(r'([st])iv$', r'\1if', r'([st])if$', r'\1iv')) +
            suffix_rules(_lang, ['aient','ais','ait','ant','ante','antes','ants','e','ent','er','es','ez','iez','ons','é','ée','ées','és'], op=RegexOp(r'c$', r'ç', r'ç$', r'c')) +
            [])
