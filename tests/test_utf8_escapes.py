# Path: tests/test_utf8_escapes.py

import os

import pytest

from umtoken.tokenizer import Tokenizer, decode_utf8_escape_words

TOKENIZER_FILE = os.path.join(os.path.dirname(__file__), "..", "assets", "ipt_32k.json")


def test_decode_words_spanning_escape():
    words = ["37", " &", "uc2b0", ";", "C"]
    assert decode_utf8_escape_words(words) == ["37", " °", "", "", "C"]


def test_decode_words_partial_overlap_and_invalid():
    # the escape ends inside a word: its tail is kept
    assert decode_utf8_escape_words(["a&", "ue284a2;b"]) == ["a™", "b"]
    # invalid UTF-8, odd hex and plain text are kept
    words = ["&uzz;", " &uc2;", " &u7", " x"]
    assert decode_utf8_escape_words(words) == words
    assert decode_utf8_escape_words(["&uc2bd;&uc2b0;"]) == ["½°"]


@pytest.fixture(scope="module")
def tokenizer():
    if not os.path.exists(TOKENIZER_FILE):
        pytest.skip("tokenizer asset not available")
    return Tokenizer.load(TOKENIZER_FILE)


def test_detokenize_opt_in(tokenizer):
    text = "bei 37 &uc2b0;C und CATHy&ue284a2; (R&D)"
    ids = tokenizer.tokenize(text)
    assert tokenizer.detokenize(ids) == text  # off by default
    tokenizer.decode_utf8_escapes = True
    try:
        out, ranges, tokens_to_words = tokenizer.detokenize(ids, return_ranges=True)
        assert out == "bei 37 °C und CATHy™ (R&D)"
        assert len(tokens_to_words) == len(ids)
        # the ranges still tile the text
        assert ranges[0][0] == 0 and sum(n for _, n in ranges) == len(out)
        assert all(a + n == b for (a, n), (b, _) in zip(ranges, ranges[1:]))
    finally:
        tokenizer.decode_utf8_escapes = False


def test_load_option():
    if not os.path.exists(TOKENIZER_FILE):
        pytest.skip("tokenizer asset not available")
    tok = Tokenizer.load(TOKENIZER_FILE, decode_utf8_escapes=True)
    assert tok.detokenize(tok.tokenize("5 &uc2b0;")) == "5 °"
