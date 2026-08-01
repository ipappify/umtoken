# Path: umtoken/langs/lv.py

from umtoken.rules import RegexOp
from umtoken.langs.utils import DEFAULT_RULES, suffix_rules, interfix_rules

_lang = 'lv'

LV_RULES = (DEFAULT_RULES + 
            suffix_rules(_lang, ['e','ei','es'], constraint_regex='[^e]$') +
            suffix_rules(_lang, ['s','si','siet','sim'], constraint_regex='([^es]|ee)$') +
            suffix_rules(_lang, ['a','ai','ais','ajai','ajam','ajiem','ajos','ajā','ajām','ajās','am','as','dama','dams','i','ie','iem','iet','ietis','ieša','ieši','iešu','im','is','iska','iski','isks','ja','jam','jams','jas','jat','ji','jiet','jis','jot','jošs','ju','jusi','juši','jām','jās','jāt','o','os','ot','t','ta','tas','ti','ties','ts','tu','tāja','tāji','tājs','tāju','u','um','uma','ums','umu','us','ā','āk','āka','ākas','āki','āko','āks','āku','ām','ās','āt','ē','ēm','ēs','ī','ība','ības','ību','īga','īgi','īgs','īgu','šana','šanas','šanu','šanā','šu','ū']) +
            suffix_rules(_lang, ['āk','ākais','ākie','āko','ākā','ākās'], op=RegexOp(r'^', r'vis', r'^vis', r'')) +
            [])
