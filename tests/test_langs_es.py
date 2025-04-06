# Path: test/test_langs_es.py

from umtoken.langs.es import ES_RULES, _lang
from umtoken.alphabet import ASCII_RESERVED_EOW as EOW
from umtoken.morpher import Morpher

from .utils import get_bases, decompose, format

def test_suffix_rules():
    examples = [
        ("casa", "cas+a"),
        ("habla", "habl+a"),
        ("hablaba", "habl+aba"),
        ("hablabas", "habl+abas"),
        ("hablabais", "habl+abais"),
        ("hablaban", "habl+aban"),
        ("hablada", "habl+ada"),
        ("habladas", "habl+adas"),
        ("hablado", "habl+ado"),
        ("hablados", "habl+ados"),
        ("hablamos", "habl+amos"),
        ("hablan", "habl+an"),
        ("hablando", "habl+ando"),
        ("hablante", "habl+ante"),
        ("hablantes", "habl+antes"),
        ("hablar", "habl+ar"),
        ("hablas", "habl+as"),
        ("hablás", "habl+ás"),
        ("habláis", "habl+áis"),
        ("hablábamos", "habl+ábamos"),
        ("come", "com+e"),
        ("comemos", "com+emos"),
        ("comes", "com+es"),
        ("comer", "com+er"),
        ("comen", "com+en"),
        ("comés", "com+és"),
        ("coméis", "com+éis"),
        ("vivida", "viv+ida"),
        ("vividas", "viv+idas"),
        ("vivido", "viv+ido"),
        ("vividos", "viv+idos"),
        ("viviendo", "viv+iendo"),
        ("viviente", "viv+iente"),
        ("vivientes", "viv+ientes"),
        ("vivimos", "viv+imos"),
        ("vivir", "viv+ir"),
        ("vivía", "viv+ía"),
        ("vivías", "viv+ías"),
        ("vivían", "viv+ían"),
        ("vivís", "viv+ís"),
        ("vivo", "viv+o"),
        ("vivos", "viv+os"),
        ("acideces", "acide[z->c]+es"),
    ]

    morpher = Morpher([_lang], get_bases(examples), rules=ES_RULES)

    for word, expected in examples:
        word = word + EOW # add end of word for suffix rules
        ids = decompose(word, morpher)
        actual = format(ids, morpher)
        assert expected in actual 

