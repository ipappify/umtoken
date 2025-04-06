# Path: test/test_langs_fr.py

from umtoken.langs.fr import FR_RULES, _lang
from umtoken.alphabet import ASCII_RESERVED_EOW as EOW
from umtoken.morpher import Morpher

from .utils import get_bases, decompose, format

def test_suffix_rules():
    examples = [
       ("mange","mang+e"),
       ("mangeait","mang+eait"),
       ("mangeant","mang+eant"),
       ("mangent","mang+ent"),
       ("mangeons","mang+eons"),
       ("manger","mang+er"),
       ("manges","mang+es"),
       ("mangez","mang+ez"),
       ("mangé","mang+é"),
       ("mangée","mang+ée"),
       ("mangées","mang+ées"),
       ("mangés","mang+és"),
       ("jouaient","jou+aient"),
       ("jouais","jou+ais"),
       ("jouait","jou+ait"),
       ("jouant","jou+ant"),
       ("fini","fin+i"),
       ("pendiez","pend+iez"),
       ("finir","fin+ir"),
       ("finis","fin+is"),
       ("finissant","fin+issant"),
       ("finissent","fin+issent"),
       ("finissons","fin+issons"),
       ("finissez","fin+issez"),
       ("finit","fin+it"),
       ("pendons","pend+ons"),
       ("maisons","maison+s"),
       ("vends","vend+s"),
       ("vendre","vend+re"),
       ("vendu","vend+u"),
       ("vendus","vend+us"),
       ("vendue","vend+ue"),
       ("vendues","vend+ues"),
       ("passif","pas[siv->sif]"),
       ("passifs","pas[siv->sif]+s"),
       ("lançaient","lan[c->ç]+aient"),
       ("lançaient","lan[c->ç]+aient"),
       ("lançant","lan[c->ç]+ant"),
       ("lançons","lan[c->ç]+ons"),
       ("principaux","princip[al->]+aux")
    ]

    morpher = Morpher([_lang], get_bases(examples), rules=FR_RULES)

    for word, expected in examples:
        word = word + EOW # add end of word for suffix rules
        ids = decompose(word, morpher)
        actual = format(ids, morpher)
        assert expected in actual 

