# Path: umtoken/langs/fr.py

from umtoken.rules import RegexOp
from umtoken.langs.utils import DEFAULT_RULES, suffix_rules, interfix_rules

_lang = 'fr'

FR_RULES = (DEFAULT_RULES + 
            suffix_rules(_lang, ['e','ea','eai','eaient','eais','eait','eant','eante','eantes','eants','eas','ement','ent','eons','er','era','erai','eraient','erais','erait','eras','erez','eriez','erions','erons','eront','es','eur','eurs','euse','euses','ez'], constraint_regex='[^e]$') +
            suffix_rules(_lang, ['s'], constraint_regex='([^es]|ee)$') +
            suffix_rules(_lang, ['a','able','ables','ai','aient','ais','ait','ant','ante','antes','ants','as','i','ie','ies','iez','ir','ira','irai','iraient','irais','irait','iras','irent','irez','iriez','irions','irons','iront','is','issaient','issais','issait','issant','issante','issantes','issants','isse','issent','isses','issez','issiez','issions','issons','it','ité','ités','ment','ons','re','u','ue','ues','us','èrent','é','ée','ées','és']) +
            suffix_rules(_lang, ['aux'], op=RegexOp(r'al$', r'', r'$', r'al')) +
            suffix_rules(_lang, ['','s'], op=RegexOp(r'([st])iv$', r'\1if', r'([st])if$', r'\1iv')) +
            suffix_rules(_lang, ['x'], constraint_regex='(au|eu|ou)$') +
            suffix_rules(_lang, ['a','ai','aient','ais','ait','ant','ante','antes','ants','as','ons'], op=RegexOp(r'c$', r'ç', r'ç$', r'c')) +
            suffix_rules(_lang, ['e','ent','era','erai','eraient','erais','erait','eras','erez','eriez','erions','erons','eront','es'], op=RegexOp(r'e([lt])$', r'e\1\1', r'e([lt])\1$', r'e\1')) +
            suffix_rules(_lang, ['e','ent','era','erai','eraient','erais','erait','eras','erez','eriez','erions','erons','eront','es'], op=RegexOp(r'e([lnrstv])$', r'è\1', r'è([lnrstv])$', r'e\1')) +
            suffix_rules(_lang, ['e','ent','es'], op=RegexOp(r'é([bcdfglmnprstv]{1,2})$', r'è\1', r'è([bcdfglmnprstv]{1,2})$', r'é\1')) +
            [])
