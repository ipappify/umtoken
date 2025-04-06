# Path: umtoken/langs/pl.py

from umtoken.rules import RegexOp
from umtoken.langs.utils import DEFAULT_RULES, suffix_rules, interfix_rules

_lang = 'pl'

PL_RULES = (DEFAULT_RULES + 
            suffix_rules(_lang, ['e','ego','ej','em','emu','en','eni','enie'], constraint_regex='[^e]$') +
            suffix_rules(_lang, ['a','ach','acie','ają','ając','ająca','ające','ający','ali','aliście','aliśmy','am','ami','amy','ana','ane','ani','anie','ano','any','asz','ać','ał','ała','ałam','ałaś','ałem','ałeś','ało','ałom','ałoś','ały','ałyście','ałyśmy','i','ia','iach','iami','iana','iane','iani','iano','iany','iał','iała','iałam','iałaś','iałem','iałeś','iało','iałom','iałoś','iały','iałyście','iałyśmy','ich','icie','ie','iego','iej','ieli','ieliście','ieliśmy','iem','iemu','ieć','ii','ili','iliście','iliśmy','im','imi','imy','io','iom','iowi','isz','iu','ią','ić','ię','ił','iła','iłam','iłaś','iłem','iłeś','iło','iłom','iłoś','iły','iłyście','iłyśmy','mi','o','om','ona','one','ono','ony','owali','owaliście','owaliśmy','owana','owane','owani','owanie','owano','owany','ować','ował','owała','owałam','owałaś','owałem','owałeś','owało','owałom','owałoś','owały','owałyście','owałyśmy','owi','u','uje','ujecie','ujemy','ujesz','ują','ując','ująca','ujące','ujący','uję','y','ych','ym','ymi','ów','ą','ąc','ąca','ące','ący','ę']) +
            suffix_rules(_lang, ['y'], op=RegexOp(r'k$', r'c', r'c$', r'k')) +
            suffix_rules(_lang, ['y'], op=RegexOp(r'g$', r'dz', r'dz$', r'g')) +
            suffix_rules(_lang, ['y'], op=RegexOp(r'r$', r'rz', r'rz$', r'r')) +
            suffix_rules(_lang, ['i'], op=RegexOp(r'ż$', r'z', r'z$', r'ż')) +
            suffix_rules(_lang, ['i'], op=RegexOp(r'sn$', r'śn', r'śn$', r'sn')) +
            suffix_rules(_lang, ['i'], op=RegexOp(r't$', r'c', r'c$', r't')) +
            suffix_rules(_lang, ['i'], op=RegexOp(r'ł$', r'l', r'l$', r'ł')) +
            suffix_rules(_lang, ['e'], op=RegexOp(r'r$', r'rz', r'rz$', r'r')) +
            [])
