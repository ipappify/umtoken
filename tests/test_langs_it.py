# Path: test/test_langs_it.py

from umtoken.langs.it import IT_RULES, _lang
from umtoken.alphabet import ASCII_RESERVED_EOW as EOW
from umtoken.morpher import Morpher

from .utils import get_bases, decompose, format

def test_suffix_rules():
    examples = [
        ("lunato", "lunat+o"),
        ("lunata", "lunat+a"),
        ("lunati", "lunat+i"),
        ("lunate", "lunat+e"),
        ("sconto", "scont+o"),
        ("sconti", "scont+i"),
        ("natura", "natur+a"),
        ("nature", "natur+e"),
        ("parlare", "parl+are"),
        ("parlando", "parl+ando"),
        ("parlante", "parl+ante"),
        ("parlanti", "parl+anti"),
        ("parlato", "parl+ato"),
        ("parlati", "parl+ati"),
        ("parlata", "parl+ata"),
        ("parlate", "parl+ate"),
        ("parlo", "parl+o"),
        ("parli", "parl+i"),
        ("parla", "parl+a"),
        ("parliamo", "parl+iamo"),
        ("parlate", "parl+ate"),
        ("parlano", "parl+ano"),
        ("parlavo", "parl+avo"),
        ("parlavi", "parl+avi"),
        ("parlava", "parl+ava"),
        ("parlavamo", "parl+avamo"),
        ("parlavate", "parl+avate"),
        ("parlavano", "parl+avano"),
        ("ricevere", "ricev+ere"),
        ("ricevendo", "ricev+endo"),
        ("ricevente", "ricev+ente"),
        ("riceventi", "ricev+enti"),
        ("ricevuto", "ricev+uto"),
        ("ricevuti", "ricev+uti"),
        ("ricevuta", "ricev+uta"),
        ("ricevute", "ricev+ute"),
        ("ricevo", "ricev+o"),
        ("ricevi", "ricev+i"),
        ("riceve", "ricev+e"),
        ("riceviamo", "ricev+iamo"),
        ("ricevete", "ricev+ete"),
        ("ricevono", "ricev+ono"),
        ("ricevevo", "ricev+evo"),
        ("ricevevi", "ricev+evi"),
        ("riceveva", "ricev+eva"),
        ("ricevevamo", "ricev+evamo"),
        ("ricevevate", "ricev+evate"),
        ("ricevevano", "ricev+evano"),
        ("dormire", "dorm+ire"),
        ("dormendo", "dorm+endo"),
        ("dormente", "dorm+ente"),
        ("dormenti", "dorm+enti"),
        ("dormito", "dorm+ito"),
        ("dormiti", "dorm+iti"),
        ("dormita", "dorm+ita"),
        ("dormite", "dorm+ite"),
        ("dormo", "dorm+o"),
        ("dormi", "dorm+i"),
        ("dorme", "dorm+e"),
        ("dormiamo", "dorm+iamo"),
        ("dormite", "dorm+ite"),
        ("dormono", "dorm+ono"),
        ("dormivo", "dorm+ivo"),
        ("dormivi", "dorm+ivi"),
        ("dormiva", "dorm+iva"),
        ("dormivamo", "dorm+ivamo"),
        ("dormivate", "dorm+ivate"),
        ("dormivano", "dorm+ivano"),
    ]

    morpher = Morpher([_lang], get_bases(examples), rules=IT_RULES)

    for word, expected in examples:
        word = word + EOW # add end of word for suffix rules
        ids = decompose(word, morpher)
        actual = format(ids, morpher)
        assert expected in actual 

