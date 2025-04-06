# Path: umtoken/langs/ro.py

from umtoken.rules import RegexOp
from umtoken.langs.utils import DEFAULT_RULES, suffix_rules, interfix_rules

_lang = 'ro'

RO_RULES = (DEFAULT_RULES + 
            suffix_rules(_lang, ['e','ea','eai','eam','eară','earăm','earăți','eat','eata','eate','eatei','eatele','eatelor','eatul','eatului','eată','eau','ează','eași','eați','eații','eaților','eează','eez','eezi','ei','ele','elor','em','ete','ez','ezi','eând','eă','eăm','eți','eții','eților'], constraint_regex='[^e]$') +
            suffix_rules(_lang, ['a','ai','am','at','atul','atule','atului','au','ați','i','ii','ile','ilor','im','ind','iră','irăm','irăți','it','iși','iți','l','le','lui','o','oasa','oase','oasei','oasele','oaselor','oasă','os','osul','osului','oși','oșii','oșilor','u','ui','ul','ului','ură','urăm','urăți','ut','uta','ute','utei','utele','utelor','utul','utului','ută','uși','uți','uții','uților','âi','âm','ând','âră','ârăm','ârăți','ât','âși','âți','î','ă','ăle','ălor','ăsc','ăște','ăști']) +
            [])
