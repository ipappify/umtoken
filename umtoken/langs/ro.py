# Path: umtoken/langs/ro.py

from umtoken.rules import RegexOp
from umtoken.langs.utils import DEFAULT_RULES, suffix_rules, interfix_rules

_lang = 'ro'

RO_RULES = (DEFAULT_RULES + 
            suffix_rules(_lang, ['e','ea','eai','eam','eară','ească','eat','eata','eate','eatei','eatele','eatelor','eatul','eatului','eată','eau','ează','eași','eați','eații','eaților','eează','eez','eezi','ei','ele','elor','em','ere','erea','eri','erile','esc','ete','ez','eze','ezi','eând','eă','eăm','ește','ești','eți','eții','eților'], constraint_regex='[^e]$') +
            suffix_rules(_lang, ['a','abil','abile','abili','abilă','ai','aj','aje','am','are','area','ară','ască','ase','asem','aseră','aseși','at','ata','ate','atei','atele','atelor','atul','atule','atului','ată','au','ași','ați','ație','ații','aților','i','ibil','ibile','ibili','ibilă','ii','ile','ilor','im','ind','ire','irea','iri','irile','iră','ise','isem','iseră','iseși','it','ita','itate','ite','itei','itele','itelor','itoare','itor','itori','itul','itului','ită','ități','iși','iți','iții','iților','l','le','lui','o','oasa','oase','oasei','oasele','oaselor','oasă','os','osul','osului','oși','oșii','oșilor','u','ui','ul','ule','ului','ură','use','usem','useră','useși','ut','uta','ute','utei','utele','utelor','utul','utului','ută','uși','uți','uții','uților','âi','âm','ând','âră','âse','âsem','âseră','âseși','ât','âte','âtă','âși','âți','î','ă','ăle','ălor','ăm','ări','ările','ăsc','ătoare','ător','ători','ăște','ăști']) +
            [])
