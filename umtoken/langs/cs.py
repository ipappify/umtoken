# Path: umtoken/langs/cs.py

from umtoken.rules import RegexOp
from umtoken.langs.utils import DEFAULT_RULES, suffix_rules, interfix_rules

_lang = 'cs'

CS_RULES = (DEFAULT_RULES + 
            suffix_rules(_lang, ['e','ech','el','ela','eli','elo','ely','em','eme','emi','en','ena','eni','eno','eny','ení','ený','et','ete','etem','eti','eň','eš'], constraint_regex='[^e]$') +
            suffix_rules(_lang, ['','a','aje','ají','ajíc','ajíce','ající','al','ala','ali','alo','aly','ami','aný','at','ata','atech','aty','atům','i','il','ila','ili','ilo','ily','in','ina','ini','ino','inou','inu','iny','iných','iným','inými','ině','it','je','jeme','jete','ješ','ji','jí','jíc','jíce','l','la','li','lo','ly','mi','na','ne','neme','nete','neš','ni','nou','nouc','nouce','noucí','nout','nu','nul','nula','nuli','nulo','nuly','nut','nuta','nuti','nuto','nuty','nutí','nutý','ní','ních','ním','ně','němi','o','ou','ouc','ouce','oucí','ova','oval','ovala','ovali','ovalo','ovaly','ovaný','ovat','ovi','ovo','ovou','ovu','ovy','ován','ována','ováni','ováno','ovány','ování','ové','ových','ovým','ovými','ově','t','u','ující','y','á','ách','ám','áme','án','ána','áni','áno','ány','ání','áte','áš','é','ého','ém','ému','í','íc','íce','ích','ící','ího','ím','íme','ími','ímu','íte','íš','ý','ých','ým','ými','ě','ěm','ěn','ěna','ěni','ěno','ěny','ění','ěný','ů','ům','ův']) +
            [])
