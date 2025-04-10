# Path: umtoken/langs/pt.py

from umtoken.rules import RegexOp
from umtoken.langs.utils import DEFAULT_RULES, suffix_rules, interfix_rules

_lang = 'pt'

PT_RULES = (DEFAULT_RULES + 
            suffix_rules(_lang, ['e','eis','em','emente','emos','endo','er','eram','es','este','estes','eu'], constraint_regex='[^e]$') +
            suffix_rules(_lang, ['a','ada','adas','ado','ados','ais','am','amente','amos','ando','ar','aram','ardes','arem','ares','armos','as','aste','astes','ava','avam','avas','i','ia','iam','ias','ida','idas','ides','ido','idos','iem','imos','indo','io','ir','iram','is','iste','istes','iu','mente','o','os','ou','uei','ámos','ávamos','áveis','íamos','íeis']) +
            suffix_rules(_lang, ['s'], op=RegexOp(r'm$', r'n', r'n$', r'm')) +
            suffix_rules(_lang, ['s'], op=RegexOp(r'l$', r'i', r'i$', r'l')) +
            suffix_rules(_lang, ['s'], op=RegexOp(r'el$', r'éi', r'éi$', r'el')) +
            suffix_rules(_lang, ['s'], op=RegexOp(r'ol$', r'ói', r'ói$', r'ol')) +
            suffix_rules(_lang, ['es'], op=RegexOp(r'ão$', r'õ', r'õ$', r'ão')) +
            [])
