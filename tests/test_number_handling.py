# Path: test/test_encoding.py

from umtoken.trainer import DEFAULT_NUMBER_SEED
from umtoken.model import EOW, SHY, Model
from umtoken.langs.utils import DEFAULT_RULES

def test_number_handling_greedy_head():
    examples = [
        ("1", ["1+X"]),
        ("12", ["12+X"]),
        ("123", ["12+", "3+X"]),
        ("1234", ["12+", "34+X"]),
        ("12345", ["12+", "34+", "5+X"]),
        ("123456", ["12+", "34+", "56+X"]),
        ("1234567", ["12+", "34+", "56+", "7+X"]),
    ]
    
    vocab = ["UNK"] + DEFAULT_NUMBER_SEED
    rules = DEFAULT_RULES

    model = Model(vocab, rules, [0.0 for _ in vocab], [0.0 for _ in rules], 
                  alpha=1.0, beta=0.0, unk_token_id=0, min_base_len=2, 
                  number_handling="greedy-head")
    
    for text, expected in examples:
        tokens = model.encode(text)
        tokens = [model.format_token(*t) for t in tokens]
        assert tokens == expected, f"For '{text}', expected {expected}, got {tokens}"
        
        
def test_number_handling_greedy_tail():
    examples = [
        ("1", ["1+X"]),
        ("12", ["12+X"]),
        ("123", ["1+", "23+X"]),
        ("1234", ["12+", "34+X"]),
        ("12345", ["1+", "23+", "45+X"]),
        ("123456", ["12+", "34+", "56+X"]),
        ("1234567", ["1+", "23+", "45+", "67+X"]),
    ]
    
    vocab = ["UNK"] + DEFAULT_NUMBER_SEED
    rules = DEFAULT_RULES

    model = Model(vocab, rules, [0.0 for _ in vocab], [0.0 for _ in rules], 
                  alpha=1.0, beta=0.0, unk_token_id=0, min_base_len=2, 
                  number_handling="greedy-tail")
    
    for text, expected in examples:
        tokens = model.encode(text)
        tokens = [model.format_token(*t) for t in tokens]
        assert tokens == expected, f"For '{text}', expected {expected}, got {tokens}"