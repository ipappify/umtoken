# Path: test/test_encoding.py

from umtoken.alphabet import Encoding, EU24_ALPHABET, MIN_ALPHABET

def test_encoding():
    examples = [
        " lower",
        " Title",
        " UPPER",
        "lower",
        "Title",
        "UPPER",
        "Ἄγειν",  # ancient Greek
        "ℚ",      # math symbol
        "火影",   # Japanese
        "𝑀𝑆𝑅",   # math italic
        "\n",     # newline
        "\t",     # tab
        "\n\n",   # multiple newlines
        "\t\t",   # multiple tabs
        " ",      # space
        "  ",     # multiple spaces
    ]
    
    enc = Encoding(EU24_ALPHABET)
    
    for example in examples:
        encoded = enc.escape(example)
        assert all(e in EU24_ALPHABET for e in encoded)
        decoded = enc.unescape(encoded)
        assert example == decoded, f"Expected '{example}', got '{decoded}'"

def test_alphabet():
    # check whether all ASCII characters in the range from 21 to 7E are in the alphabet (excluding uppercase letters)
    assert all(chr(i) in MIN_ALPHABET for i in range(0x21, 0x7E) if chr(i).islower())