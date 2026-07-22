# Path: umtoken/langs/lt.py

from umtoken.rules import RegexOp
from umtoken.langs.utils import DEFAULT_RULES, suffix_rules, interfix_rules

_lang = 'lt'

LT_RULES = (DEFAULT_RULES + 
            suffix_rules(_lang, ['e','ei','es','esni','esnio','esnis','esnė','esnės'], constraint_regex='[^e]$') +
            suffix_rules(_lang, ['s','si','sime','site','siu'], constraint_regex='([^es]|ee)$') +
            suffix_rules(_lang, ['a','ai','ais','am','ama','amas','ame','ams','ant','anti','antis','as','ate','au','aus','dama','damas','dami','davai','davau','davo','davome','davote','i','iai','iais','iams','iau','iausi','iausia','iausiai','iausias','iausio','iausios','iems','ima','imai','imas','imo','imą','imų','iniai','inis','inių','inė','io','is','iu','iui','iuose','ius','iška','iškai','iškas','ių','jau','jo','jome','k','kime','kite','mas','mo','mą','o','oje','ome','omis','oms','os','ose','ote','ta','tas','ti','tojai','tojas','tojo','toją','tojų','tos','tum','tume','tumėte','tus','tų','u','ui','uje','umas','umi','umis','umo','ums','umą','uose','us','usi','yje','ys','ystė','ystės','ystę','ą','čiau','ė','ėje','ėmis','ėms','ės','ėse','ę','ęs','į','ūs','ų']) +
            [])
