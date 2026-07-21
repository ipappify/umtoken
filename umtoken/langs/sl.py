# Path: umtoken/langs/sl.py

from umtoken.rules import RegexOp
from umtoken.langs.utils import DEFAULT_RULES, suffix_rules, interfix_rules

_lang = 'sl'

SL_RULES = (DEFAULT_RULES + 
            suffix_rules(_lang, ['e','ega','eh','eje','ejša','ejše','ejšega','ejšem','ejšemu','ejši','ejših','ejšim','ejšimi','ejšo','el','ela','ele','eli','elo','em','ema','emu','en','ena','eni','enih','enom','enu','eti','ev','eva','eve','evega','evem','evemu','evi','evih','evim','evimi','evo'], constraint_regex='[^e]$') +
            suffix_rules(_lang, ['ska','ske','skega','skem','skemu','ski','skih','skim','skimi','sko'], constraint_regex='([^es]|ee)$') +
            suffix_rules(_lang, ['a','ah','aj','ajmo','ajo','ajta','ajte','ajva','al','ala','ale','ali','alo','am','ama','ami','amo','an','ana','ane','ani','anje','ano','at','ata','ate','ati','ava','aš','i','ica','icah','icam','icami','ice','ici','ico','ih','ijo','il','ila','ile','ili','ilo','im','ima','imi','imo','in','ina','ine','inega','inem','inemu','ini','inih','inim','inimi','ino','it','ita','ite','iti','iva','iš','jen','jena','jene','jeni','jenje','jeno','jo','ljiv','ljiva','ljive','ljivi','ljivo','mi','ne','nejo','nem','nemo','neta','nete','neva','neš','ni','nil','nila','nile','nili','nilo','nimo','nite','niti','njen','njena','njene','njeni','njeno','o','om','oma','ost','osti','ostih','ostjo','ostmi','ov','ova','oval','ovala','ovale','ovali','ovalo','ovan','ovana','ovane','ovani','ovanje','ovano','ovati','ove','ovega','ovem','ovemu','ovi','ovih','ovim','ovimi','ovo','telj','telja','teljem','teljev','telji','telju','u','uj','uje','ujejo','ujem','ujemo','ujeta','ujete','ujeva','uješ','ujmo','ujte','ša','še','šega','šem','šemu','ši','ših','šim','šimi','šo']) +
            suffix_rules(_lang, ['eje','ejša','ejše','ejši','ša','še','ši'], op=RegexOp(r'^', r'naj', r'^naj', r'')) +
            suffix_rules(_lang, ['i'], op=RegexOp(r'k$', r'c', r'c$', r'k')) +
            interfix_rules(_lang, ['o']) +
            [])
