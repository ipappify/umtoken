# Path: umtoken/langs/mt.py

from umtoken.rules import RegexOp
from umtoken.langs.utils import DEFAULT_RULES, suffix_rules, interfix_rules

_lang = 'mt'

MT_RULES = (DEFAULT_RULES + 
            suffix_rules(_lang, ['ejn','ek','et'], constraint_regex='[^e]$') +
            suffix_rules(_lang, ['a','ajiet','ajna','ajt','ajtu','ar','at','ata','ati','aw','azzjoni','azzjonijiet','ha','hom','i','iet','ijiet','in','it','ita','iti','ixxa','ixxejna','ixxejt','ixxew','ixxi','ka','kom','ku','na','t','tejn','tu','u','uż','uża','użi','x','ċi']) +
            [])
