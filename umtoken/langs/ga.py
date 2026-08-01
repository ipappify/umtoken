# Path: umtoken/langs/ga.py

from umtoken.rules import RegexOp
from umtoken.langs.utils import DEFAULT_RULES, suffix_rules, interfix_rules

_lang = 'ga'

GA_RULES = (DEFAULT_RULES + 
            suffix_rules(_lang, ['e','each','eacha','eacht','eadh','eann','eanna','eoidh'], constraint_regex='[^e]$') +
            suffix_rules(_lang, ['a','ach','acha','acht','adh','aigí','aimid','aithe','ann','anna','aí','aígí','aímid','aíonn','aítear','dóir','faidh','faimid','far','fear','fidh','fimid','igí','imid','ithe','iú','iúil','mhar','t','ta','tar','te','tear','teoir','tóir','áil','í','ígí','ímid','ín','íonn','ítear','ófar','óidh','ú']) +
            suffix_rules(_lang, ['amar','aíomar','eamar','eodh','fadh','feadh','ódh'], op=RegexOp(r'^([bcdfgmpst])([^h])', r'\1h\2', r'^([bcdfgmpst])h', r'\1')) +
            [])
