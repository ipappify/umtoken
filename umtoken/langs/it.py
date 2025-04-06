# Path: umtoken/langs/it.py

from umtoken.rules import RegexOp
from umtoken.langs.utils import DEFAULT_RULES, suffix_rules, interfix_rules

_lang = 'it'

IT_RULES = (DEFAULT_RULES + 
            suffix_rules(_lang, ['e','emente','endo','ente','enti','ere','ete','eva','evamo','evano','evate','evi','evo'], constraint_regex='[^e]$') +
            suffix_rules(_lang, ['a','amente','ando','ano','ante','anti','are','ata','ate','ati','ato','ava','avamo','avano','avate','avi','avo','i','iamo','ire','ita','ite','iti','ito','iva','ivamo','ivano','ivate','ivi','ivo','mente','o','ono','uta','ute','uti','uto']) +
            [])
