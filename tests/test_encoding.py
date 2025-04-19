# Path: test/test_encoding.py

from umtoken.alphabet import Encoding, EU24_ALPHABET, MIN_ALPHABET, ASCII_RESERVED_UTF8, ASCII_RESERVED_HEX, ASCII_RESERVED_UPPER

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
    
    allowed_chars = EU24_ALPHABET + ASCII_RESERVED_UTF8 + ASCII_RESERVED_HEX + ASCII_RESERVED_UPPER
    
    for example in examples:
        encoded = enc.escape(example)
        assert all(e in allowed_chars for e in encoded)
        decoded = enc.unescape(encoded)
        assert example == decoded, f"Expected '{example}', got '{decoded}'"

def test_alphabet():
    # check whether all ASCII characters in the range from 21 to 7E are in the alphabet (excluding uppercase letters)
    assert all(chr(i) in MIN_ALPHABET for i in range(0x21, 0x7E) if chr(i).islower())