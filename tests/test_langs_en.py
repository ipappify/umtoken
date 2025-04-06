# Path: test/test_langs_en.py

from umtoken.langs.en import EN_RULES, _lang
from umtoken.alphabet import ASCII_RESERVED_EOW as EOW
from umtoken.morpher import Morpher

from .utils import get_bases, decompose, format

def test_suffix_rules():
    examples = [
        ("tries", "tr[y->i]+es"),
        ("house", "hous+e"),
        ("houses", "hous+es"),
        ("loved", "lov+ed"),
        ("nicer", "nic+er"),
        ("lovers", "lov+ers"),
        ("nicely", "nic+ely"),
        ("nicest", "nic+est"),
        ("days", "day+s"),
        ("trees", "tree+s"),
        ("proudly", "proud+ly"),
        ("loving", "lov+ing"),
        ("feelings", "feel+ings"),
        ("lovable", "lov+able"),
        ("executables", "execut+ables"),
        ("executably", "execut+ably"),
        ("studied", "stud[y->i]+ed"),
        ("running", "ru[n->nn]+ing"),
        ("runnings", "ru[n->nn]+ings"),
        ("controller", "contro[l->ll]+er"),
        ("controllers", "contro[l->ll]+ers"),
        ("controllable", "contro[l->ll]+able"),
        ("controllables", "contro[l->ll]+ables"),
        ("controllably", "contro[l->ll]+ably"),
    ]

    morpher = Morpher([_lang], get_bases(examples), rules=EN_RULES)

    for word, expected in examples:
        word = word + EOW # add end of word for suffix rules
        ids = decompose(word, morpher)
        actual = format(ids, morpher)
        assert expected in actual 

