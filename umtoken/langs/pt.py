# Path: umtoken/langs/pt.py

from umtoken.rules import RegexOp
from umtoken.langs.utils import DEFAULT_RULES, suffix_rules, interfix_rules

_lang = 'pt'

PT_RULES = (DEFAULT_RULES + 
            suffix_rules(_lang, ['e','edor','edora','edoras','edores','ei','em','emente','emos','endo','er','eram','erei','erem','eremos','eres','eria','eriam','erias','ermos','erá','erás','erão','eríamos','es','esse','essem','esses','este','eu'], constraint_regex='[^e]$') +
            suffix_rules(_lang, ['a','ada','adas','ado','ador','adora','adoras','adores','ados','agem','agens','am','amente','amos','ando','ar','aram','arei','arem','aremos','ares','aria','ariam','arias','armos','ará','arás','arão','aríamos','as','asse','assem','asses','aste','ava','avam','avas','ação','ações','i','ia','iam','ias','ida','idade','idades','idas','ido','idos','imos','indo','ir','iram','irei','irem','iremos','ires','iria','iriam','irias','irmos','irá','irás','irão','iríamos','isse','issem','isses','iste','iu','mente','o','os','ou','ámos','ávamos','áveis','ável','íamos','íveis','ível']) +
            suffix_rules(_lang, ['s'], op=RegexOp(r'm$', r'n', r'n$', r'm')) +
            suffix_rules(_lang, ['s'], op=RegexOp(r'l$', r'i', r'i$', r'l')) +
            suffix_rules(_lang, ['s'], op=RegexOp(r'el$', r'éi', r'éi$', r'el')) +
            suffix_rules(_lang, ['s'], op=RegexOp(r'ol$', r'ói', r'ói$', r'ol')) +
            suffix_rules(_lang, ['es'], op=RegexOp(r'ão$', r'õ', r'õ$', r'ão')) +
            suffix_rules(_lang, ['es'], op=RegexOp(r'ão$', r'ã', r'ã$', r'ão')) +
            suffix_rules(_lang, ['e','ei','em','emos','es'], op=RegexOp(r'c$', r'qu', r'qu$', r'c')) +
            suffix_rules(_lang, ['e','ei','em','emos','es'], op=RegexOp(r'g$', r'gu', r'gu$', r'g')) +
            suffix_rules(_lang, ['e','ei','em','emos','es'], op=RegexOp(r'ç$', r'c', r'c$', r'ç')) +
            [])
