# Path: umtoken/langs/it.py

from umtoken.rules import RegexOp
from umtoken.langs.utils import DEFAULT_RULES, suffix_rules, interfix_rules

_lang = 'it'

IT_RULES = (DEFAULT_RULES + 
            suffix_rules(_lang, ['e','ei','emente','emmo','endo','ente','enti','ere','erono','este','esti','ete','ette','ettero','etti','eva','evamo','evano','evate','evi','evo'], constraint_regex='[^e]$') +
            suffix_rules(_lang, ['a','ai','amente','ammo','ando','ano','ante','anti','are','arono','aste','asti','ata','ate','ati','ato','ava','avamo','avano','avate','avi','avo','i','iamo','ii','immo','ire','irono','isce','isci','isco','iscono','iste','isti','ita','ite','iti','ito','iva','ivamo','ivano','ivate','ivi','ivo','mente','o','ono','uta','ute','uti','uto','é','ò']) +
            [])
