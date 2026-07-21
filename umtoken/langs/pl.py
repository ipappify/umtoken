# Path: umtoken/langs/pl.py

from umtoken.rules import RegexOp
from umtoken.langs.utils import DEFAULT_RULES, suffix_rules, interfix_rules

_lang = 'pl'

PL_RULES = (DEFAULT_RULES + 
            suffix_rules(_lang, ['e','ego','ej','ek','em','emu','en','eni','enie'], constraint_regex='[^e]$') +
            suffix_rules(_lang, ['scy','si','ska','ski','skich','skie','skiego','skiej','skiemu','skim','skimi','ską','sza','sze','szy'], constraint_regex='([^es]|ee)$') +
            suffix_rules(_lang, ['a','ach','acie','acz','acza','acze','aczy','aj','ajcie','ajmy','ają','ając','ająca','ające','ający','ali','aliby','aliście','aliśmy','alna','alne','alny','am','ami','amy','ana','ane','ani','anie','ano','any','asz','ać','ał','ała','ałaby','ałam','ałaś','ałby','ałem','ałeś','ało','ałoby','ały','ałyby','ałyście','ałyśmy','ce','i','ia','iach','iami','iana','iane','iani','iano','iany','iał','iała','iałaby','iałam','iałaś','iałby','iałem','iałeś','iało','iałoby','iały','iałyby','iałyście','iałyśmy','ich','icie','ie','iego','iej','iejsza','iejsze','iejszy','ieli','ieliby','ieliście','ieliśmy','iem','iemu','ieć','ii','ili','iliby','iliście','iliśmy','im','imi','imy','io','iom','iowi','isz','iu','ią','ić','ię','ił','iła','iłaby','iłam','iłaś','iłby','iłem','iłeś','iło','iłoby','iły','iłyby','iłyście','iłyśmy','ka','kach','kami','ki','kom','ką','kę','mi','nie','niecie','niemy','niesz','nij','nijcie','nijmy','nięci','nięcie','nięta','nięte','nięto','nięty','ną','nąc','nąć','nął','nę','nęli','nęła','nęło','nęły','o','om','ona','one','ono','ony','owa','owali','owaliby','owaliście','owaliśmy','owana','owane','owani','owanie','owano','owany','ować','ował','owała','owałaby','owałam','owałaś','owałby','owałem','owałeś','owało','owałoby','owały','owałyby','owałyście','owałyśmy','owe','owego','owej','owemu','owi','owie','owy','owych','owym','owymi','ową','ości','ościach','ościami','ościom','ością','ość','u','uj','ujcie','uje','ujecie','ujemy','ujesz','ujmy','ują','ując','ująca','ujące','ujący','uję','y','ych','ym','ymi','ów','ą','ąc','ąca','ące','ący','ę']) +
            suffix_rules(_lang, ['y'], op=RegexOp(r'k$', r'c', r'c$', r'k')) +
            suffix_rules(_lang, ['y'], op=RegexOp(r'g$', r'dz', r'dz$', r'g')) +
            suffix_rules(_lang, ['y'], op=RegexOp(r'r$', r'rz', r'rz$', r'r')) +
            suffix_rules(_lang, ['i'], op=RegexOp(r'ż$', r'z', r'z$', r'ż')) +
            suffix_rules(_lang, ['i'], op=RegexOp(r'sn$', r'śn', r'śn$', r'sn')) +
            suffix_rules(_lang, ['i'], op=RegexOp(r't$', r'c', r'c$', r't')) +
            suffix_rules(_lang, ['i'], op=RegexOp(r'ł$', r'l', r'l$', r'ł')) +
            suffix_rules(_lang, ['iej','iejsza','iejsze','iejszy','si','sza','sze','szy'], op=RegexOp(r'^', r'naj', r'^naj', r'')) +
            suffix_rules(_lang, ['e'], op=RegexOp(r'r$', r'rz', r'rz$', r'r')) +
            [])
