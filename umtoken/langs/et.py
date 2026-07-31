# Path: umtoken/langs/et.py

from umtoken.rules import RegexOp
from umtoken.langs.utils import DEFAULT_RULES, suffix_rules, interfix_rules

_lang = 'et'

ET_RULES = (DEFAULT_RULES + 
            suffix_rules(_lang, ['b','d','da','de','dega','deks','del','dele','delt','des','desse','dest','dud','dus','duse','dust','ga','ge','gu','i','id','im','ima','imad','ja','jad','jaid','jate','ks','ksid','ksime','ksin','ksite','l','lane','lase','lased','lasi','last','laste','le','lik','liku','likud','line','lise','list','lt','m','ma','mad','mas','mast','mat','mata','me','mine','mise','mised','mist','miste','n','na','ni','nud','t','ta','takse','tav','te','tega','teks','tel','tele','telt','tena','teni','tes','tesse','test','teta','ti','tu','tud','us','use','used','ust','uste','v','vad']) +
            suffix_rules(_lang, ['sti'], constraint_regex='[^s]$') +
            suffix_rules(_lang, ['s','sid','sse','st'], constraint_regex='[^s]$') +
            suffix_rules(_lang, ['ne','se','sed','si','st','ste'], constraint_regex='[^s]$') +
            suffix_rules(_lang, ['a','i','u'], op=RegexOp(r'([aeiouõäöü])([kpt])\2$', r'\1\2', r'([aeiouõäöü])([kpt])$', r'\1\2\2')) +
            suffix_rules(_lang, ['s','sid','sime','sin','site'], constraint_regex='[^s]$') +
            [])
