# path: tests/utils.py

from typing import List, Tuple

from umtoken.utils import format
from umtoken.morpher import Morpher

def get_bases(examples: List[Tuple[str, str]]):
    bases = set()
    for _, x in examples:
        x = x.split("+")[0]
        if "[" in x:
            x, y = x.split("[")
            y = y.split("-")[0]
            bases.add(x + y)
        else:
            bases.add(x)
    return list(bases)

def decompose(word: str, morpher: Morpher):
    return list(x for x in morpher.decompose(word, langs=None) if x[3] == len(word))
