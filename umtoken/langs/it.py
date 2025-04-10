# Path: umtoken/langs/it.py

from umtoken.rules import RegexOp
from umtoken.langs.utils import DEFAULT_RULES, suffix_rules, interfix_rules

_lang = 'it'

IT_RULES = (DEFAULT_RULES + 
            suffix_rules(_lang, ['e','emente','evàmo','evàte'], constraint_regex='[^e]$') +
            suffix_rules(_lang, ['a','amente','ano','avàmo','avàte','i','ivàmo','ivàte','iàmo','mente','o','ono','ài','àmmo','àndo','ànte','ànti','àre','àrono','àste','àsti','àta','àte','àti','àto','àva','àvano','àvi','àvo','èndo','ènte','ènti','é','éi','émmo','ére','érono','éste','ésti','éte','étte','éttero','étti','éva','évano','évi','évo','ì','ìi','ìmmo','ìre','ìrono','ìsce','ìsci','ìsco','ìscono','ìste','ìsti','ìta','ìte','ìti','ìto','ìva','ìvano','ìvi','ìvo','ò','ùta','ùte','ùti','ùto']) +
            [])
