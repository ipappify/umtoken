# Path: test/test_langs_de.py

from umtoken.langs.de import DE_RULES, _lang
from umtoken.alphabet import ASCII_RESERVED_EOW as EOW
from umtoken.morpher import Morpher

from .utils import get_bases, decompose, format

def test_suffix_rules():
    examples = [
        ("Blume", "Blum+e"),
        ("Blumen", "Blum+en"),
        ("gutem", "gut+em"),
        ("guter", "gut+er"),
        ("gutes", "gut+es"),
        ("Bildern", "Bild+ern"),
        ("geladene", "gelad+ene"),
        ("geladenen", "gelad+enen"),
        ("geladenem", "gelad+enem"),
        ("geladener", "gelad+ener"),
        ("geladenes", "gelad+enes"),
        ("Klees", "Klee+s"),
        ("Baums", "Baum+s"),
        ("Lehrerinnen", "Lehrerin+nen"),
        ("kritzeln", "kritzel+n"),
        ("sagt", "sag+t"),
        ("sagst", "sag+st"),
        ("sagte", "sag+te"),
        ("sagten", "sag+ten"),
        ("besagten", "besag+ten"),
        ("besagtem", "besag+tem"),
        ("besagter", "besag+ter"),
        ("besagtes", "besag+tes"),
        ("deutet", "deut+et"),
        ("deutest", "deut+est"),
        ("deutete", "deut+ete"),
        ("gedeuteten", "gedeut+eten"),
        ("gedeutetem", "gedeut+etem"),
        ("gedeuteter", "gedeut+eter"),
        ("gedeutetes", "gedeut+etes"),
        ("Umgebung", "Umgeb+ung"),
        ("Umgebungen", "Umgeb+ungen"),
    ]

    morpher = Morpher([_lang], get_bases(examples), rules=DE_RULES)

    for word, expected in examples:
        word = word + EOW # add end of word for suffix rules
        ids = decompose(word, morpher)
        actual = format(ids, morpher)
        assert expected in actual 

def test_interfix_rules():
    examples = [
        ("Binde", "Bind+e"),
        ("Bilder", "Bild+er"),
        ("Blumen", "Blum+en"),
        ("Lebens", "Leb+ens"),
        ("Tages", "Tag+es"),
        ("Aktivitäts", "Aktivität+s"),
        ("Tagungs", "Tag+ungs"),
    ]

    morpher = Morpher([_lang], get_bases(examples), rules=DE_RULES)

    for word, expected in examples:
        word = word # no end of word for interfix rules
        ids = decompose(word, morpher)
        actual = format(ids, morpher)
        assert expected in actual 