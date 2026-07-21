# Path: umtoken/langs/hr.py

from umtoken.rules import RegexOp
from umtoken.langs.utils import DEFAULT_RULES, suffix_rules, interfix_rules

_lang = 'hr'

HR_RULES = (DEFAULT_RULES + 
            suffix_rules(_lang, ['e','em','en','ena','ene','eni','enima','enje','eno','enom','enu','eta','etom','etu','ev','eva','eve','evi','evih','evim','evima','evo','evog','evom','evu','eći'], constraint_regex='[^e]$') +
            suffix_rules(_lang, ['ska','ske','ski','skih','skim','skima','sko','skog','skoj','skom','sku'], constraint_regex='([^es]|ee)$') +
            suffix_rules(_lang, ['a','aj','ajmo','ajte','aju','ajući','ala','ale','ali','alo','am','ama','amo','an','ana','ane','ani','anje','ano','ao','ate','ati','aš','i','ica','icama','ice','ici','icom','icu','ih','ija','ije','ijeg','ijem','iji','ijih','ijim','ijima','ijoj','ijom','iju','ila','ile','ili','ilo','im','ima','imo','in','ina','ine','ini','inih','inim','inima','ino','inog','inom','inu','io','ite','iti','iv','iva','ivo','iš','jela','jele','jeli','jelo','jeti','ju','ljen','ljena','ljene','ljeni','ljeno','ljiv','ljiva','ljive','ljivi','ljivo','ne','nem','nemo','nete','neš','ni','nimo','nite','nu','nula','nule','nuli','nulo','nuo','nut','nuta','nute','nuti','nuto','o','og','oga','oj','om','ome','omu','ost','osti','ostima','ov','ova','ovala','ovale','ovali','ovalo','ovan','ovana','ovane','ovani','ovanje','ovano','ovao','ovati','ove','ovi','ovih','ovim','ovima','ovo','ovog','ovom','ovu','telj','telja','telje','teljem','telji','teljima','telju','u','uj','uje','ujem','ujemo','ujete','uješ','ujmo','ujte','uju','ujući','ša','še','šeg','šem','ši','ših','šim','šima','šoj','šom','šu']) +
            suffix_rules(_lang, ['ija','ije','ijeg','ijem','iji','ijih','ijim','ijima','ijoj','ijom','iju','ša','še','ši'], op=RegexOp(r'^', r'naj', r'^naj', r'')) +
            suffix_rules(_lang, ['i','ima'], op=RegexOp(r'k$', r'c', r'c$', r'k')) +
            suffix_rules(_lang, ['i','ima'], op=RegexOp(r'g$', r'z', r'z$', r'g')) +
            suffix_rules(_lang, ['i','ima'], op=RegexOp(r'h$', r's', r's$', r'h')) +
            suffix_rules(_lang, ['e'], op=RegexOp(r'k$', r'č', r'č$', r'k')) +
            suffix_rules(_lang, ['e'], op=RegexOp(r'g$', r'ž', r'ž$', r'g')) +
            suffix_rules(_lang, ['e'], op=RegexOp(r'h$', r'š', r'š$', r'h')) +
            interfix_rules(_lang, ['o']) +
            [])
