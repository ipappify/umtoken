# Path: umtoken/langs/cs.py

from umtoken.rules import RegexOp
from umtoken.langs.utils import DEFAULT_RULES, suffix_rules, interfix_rules

_lang = 'cs'

CS_RULES = (DEFAULT_RULES + 
            suffix_rules(_lang, ['e','ech','ej','eji','ejme','ejte','ejší','ek','el','ela','eli','elo','ely','em','eme','emi','en','ena','eni','eno','eny','ení','ený','et','ete','etem','eti','eň','eš'], constraint_regex='[^e]$') +
            suffix_rules(_lang, ['skou','ská','ské','ského','ském','skému','ský','ských','ským','skými'], constraint_regex='([^es]|ee)$') +
            suffix_rules(_lang, ['a','ají','ající','al','ala','ali','alo','aly','ami','aný','at','ata','atech','aty','atům','ce','i','il','ila','ili','ilo','ily','in','ina','ini','ino','inou','inu','iny','iných','iným','inými','ině','it','j','je','jeme','jete','ješ','ji','jme','jte','jí','ka','kami','kou','ku','ky','kách','kám','l','la','li','lo','ly','mi','ne','neme','nete','neš','ni','nou','noucí','nout','nu','nul','nula','nuli','nulo','nuly','nut','nuta','nuti','nuto','nuty','nutí','nutý','ní','ních','ním','ně','něme','němi','něte','o','ost','ostech','ostem','osti','ostmi','ostí','ou','oucí','ova','oval','ovala','ovali','ovalo','ovaly','ovaný','ovat','ovi','ovo','ovou','ovu','ovy','ová','ován','ována','ováni','ováno','ovány','ování','ové','ového','ovém','ovému','ový','ových','ovým','ovými','ově','t','tel','tele','telná','telné','telný','telé','telů','telům','u','uj','uje','ujeme','ujete','uješ','uji','ujme','ujte','ují','ující','y','á','ách','ám','áme','án','ána','áni','áno','ány','ání','áte','áš','é','ého','ém','ému','í','ích','ící','ího','ím','íme','ími','ímu','íte','íš','ý','ých','ým','ými','ě','ěji','ější','ěm','ěn','ěna','ěni','ěno','ěny','ění','ěný','ští','ší','ů','ům','ův']) +
            suffix_rules(_lang, ['eji','ejší','ěji','ější','ší'], op=RegexOp(r'^', r'nej', r'^nej', r'')) +
            [])
