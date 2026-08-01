# Path: umtoken/langs/sk.py

from umtoken.rules import RegexOp
from umtoken.langs.utils import DEFAULT_RULES, suffix_rules, interfix_rules

_lang = 'sk'

SK_RULES = (DEFAULT_RULES + 
            suffix_rules(_lang, ['e','eho','ej','ejú','ejšia','ejšie','ejší','el','ela','eli','elo','emu','enie','ená','ené','ení','ený'], constraint_regex='[^e]$') +
            suffix_rules(_lang, ['skom','skou','ská','ské','ského','skému','skí','skú','ský','ských','ským','skými'], constraint_regex='([^es]|ee)$') +
            suffix_rules(_lang, ['a','aj','ajme','ajte','ajú','ajúci','al','ala','ali','alo','am','ame','ami','anie','aná','ané','aní','aný','at','atami','ate','ati','atá','atách','atám','aš','ať','aťa','aťom','aťu','i','ia','iach','iaci','iam','iami','ie','ieho','iem','ieme','iemu','iete','ieš','ieť','il','ila','ili','ilo','im','ime','in','ina','ine','inej','inho','ini','inmu','ino','inom','inou','inu','iných','iným','inými','ite','iu','iš','iť','ka','kami','ke','kou','ku','ky','kách','kám','la','li','lo','mi','ne','nem','neme','nete','neš','ni','nime','nite','nú','núť','o','och','ol','om','osti','ostiach','ostiam','ostí','osť','osťami','osťou','ou','ov','ova','oval','ovala','ovali','ovalo','ovanie','ovaná','ované','ovaní','ovaný','ovať','ove','ovej','ovho','ovi','ovia','ovmu','ovo','ovom','ovou','ovu','ová','ové','ového','ovému','ový','ových','ovým','ovými','telia','teľ','teľa','teľná','teľné','teľný','teľom','teľov','teľovi','u','uj','uje','ujem','ujeme','ujete','uješ','ujme','ujte','ujú','ujúci','ul','ula','uli','ulo','utie','utá','uté','utý','y','ych','ym','ymi','á','ách','ám','áme','áte','áš','é','ého','ému','í','ích','ím','íme','ími','íte','íš','ú','úť','ý','ých','ým','ými','šej','šia','šie','šieho','šiemu','šiu','šom','šou','ší','ších','ším','šími']) +
            suffix_rules(_lang, ['ejšia','ejšie','ejší','šia','šie','ší'], op=RegexOp(r'^', r'naj', r'^naj', r'')) +
            suffix_rules(_lang, ['i'], op=RegexOp(r'k$', r'c', r'c$', r'k')) +
            suffix_rules(_lang, ['i'], op=RegexOp(r'ch$', r's', r's$', r'ch')) +
            interfix_rules(_lang, ['e'], constraint_regex='[^e]$') +
            interfix_rules(_lang, ['o']) +
            [])
