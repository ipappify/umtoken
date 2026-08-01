# Path: umtoken/langs/it.py

from umtoken.rules import RegexOp
from umtoken.langs.utils import DEFAULT_RULES, suffix_rules, interfix_rules

_lang = 'it'

IT_RULES = (DEFAULT_RULES + 
            suffix_rules(_lang, ['e','ei','emente','emmo','endo','ente','enti','erai','eranno','ere','erebbe','erebbero','erei','eremmo','eremo','ereste','eresti','erete','erono','erà','erò','esse','essero','essi','este','esti','ete','ette','ettero','etti','eva','evamo','evano','evate','evi','evo'], constraint_regex='[^e]$') +
            suffix_rules(_lang, ['a','abile','abili','aggi','aggio','ai','amente','amenti','amento','ammo','ando','ano','ante','anti','are','arono','asse','assero','assi','aste','asti','ata','ate','ati','ato','atore','atori','atrice','atrici','ava','avamo','avano','avate','avi','avo','azione','azioni','i','iamo','iate','ibile','ibili','iente','ienti','ii','imenti','imento','immo','ino','irai','iranno','ire','irebbe','irebbero','irei','iremmo','iremo','ireste','iresti','irete','irono','irà','irò','isca','iscano','isce','isci','isco','iscono','isse','issero','issi','issima','issime','issimi','issimo','iste','isti','ita','ite','iti','ito','ità','iva','ivamo','ivano','ivate','ivi','ivo','mente','o','ono','uta','ute','uti','uto','é','ì','ò']) +
            suffix_rules(_lang, ['e','erai','eranno','erebbe','erebbero','erei','eremmo','eremo','ereste','eresti','erete','erà','erò','i','iamo','ino'], op=RegexOp(r'c$', r'ch', r'ch$', r'c')) +
            suffix_rules(_lang, ['e','erai','eranno','erebbe','erebbero','erei','eremmo','eremo','ereste','eresti','erete','erà','erò','i','iamo','ino'], op=RegexOp(r'g$', r'gh', r'gh$', r'g')) +
            [])
