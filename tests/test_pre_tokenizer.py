# Path: test/test_pre_tokenizer.py

from umtoken.alphabet import EU24_ALPHABET
from umtoken.pre import PreTokenizer

def test_split():
    examples = [
        "Resistivity is_commonly represented  by the Greek letter ρ (rho). The SI unit of electrical resistivity is the ohm-meter (Ω⋅m).",
        "   indentation",
        "\n\nnew paragraph",
        "\t\t\ttabbed text",
        "### heading 3",
    ]
    
    pre = PreTokenizer(alphabet=EU24_ALPHABET, normalization="ipt")
    for example in examples:
        words = pre.split(example)
        assert len(words) > 1, "Text should be split into multiple words"
        assert example == "".join(words), "Rejoining the split words should result in the original text"
        
def test_normalize_default_preserve():
    examples = [
        ("º", "º"),
        ("X̅", "X̅"),
        ("\u00AD", "\u00AD"),
        ("\n", "\n"),
        ("ρ", "ρ"),
        ("\f", " "),
        ("\t", "\t"),
        (" ", " "),
        ("İ".lower(), "İ".lower()), 
        ("\u200b", "\u200b"),
    ]
    pre = PreTokenizer(alphabet=EU24_ALPHABET, normalization="default", preserve_soft_hyphen=True, preserve_format_and_diactritic=True)
    for example, expected in examples:
        actual = pre.normalize(example)
        assert actual == expected, f"Expected {expected}, got {actual}"
        
def test_normalize_ipt_preserve():
    examples = [
        ("º", "o"),
        ("X̅", "X̅"),
        ("\u00AD", "\u00AD"),
        ("\n", "\n"),
        ("ρ", "ρ"),
        ("\f", " "),
        ("\t", "\t"),
        (" ", " "),
        ("İ".lower(), "İ".lower()), 
        ("\u200b", "\u200b"),
    ]
    pre = PreTokenizer(alphabet=EU24_ALPHABET, normalization="ipt", preserve_soft_hyphen=True, preserve_format_and_diactritic=True)
    for example, expected in examples:
        actual = pre.normalize(example)
        assert actual == expected, f"Expected {expected}, got {actual}"
        
def test_normalize_ipt_no_preserve():
    examples = [
        ("º", "o"),
        ("X̅", "X"),
        ("\u00AD", ""),
        ("\n", "\n"),
        ("ρ", "ρ"),
        ("\f", " "),
        ("\t", "\t"),
        (" ", " "),
        ("İ".lower(), "i"), 
        ("\u200b", ""),
    ]
    pre = PreTokenizer(alphabet=EU24_ALPHABET, normalization="ipt", preserve_soft_hyphen=False, preserve_format_and_diactritic=False)
    for example, expected in examples:
        actual = pre.normalize(example)
        assert actual == expected, f"Expected {expected}, got {actual}"
        
def test_escape():
    examples = [
        ("    ", "GGGG"),
        ("\n\n", "NN"),
        (" ws", "Gws"),
        ("ρ", "ρ"),
        ("UNRESERVED", "UUunreserved"),
        ("RESERVED", "RESERVED"),
        ("火影", "VE781ABWVE5BDB1W"),
    ]
    pre = PreTokenizer(alphabet=EU24_ALPHABET, normalization="ipt", reserved_tokens=["RESERVED"])
    for example, expected in examples:
        actual = pre.escape(example, handle_reserved=True)
        assert actual == expected, f"Expected {expected}, got {pre.escape(example)}"
        
def test_split_and_escape():
    examples = [
        "    indentation", 
        "Resistivity is_commonly represented by the Greek letter ρ (rho). The SI unit of electrical resistivity is the ohm-meter (Ω⋅m)."
    ]
    
    pre = PreTokenizer(alphabet=EU24_ALPHABET, normalization="ipt")
    for example in examples:
        words, ranges = pre.split_and_escape(example, return_ranges=True)
        assert len(words) > 1, "Text should be split into multiple words"
        assert len(words) == len(ranges), "Each word should have a corresponding range"
        unescaped_words = [pre.unescape(word) for word in words]
        original_words = [example[start:start+length] for start, length in ranges]
        assert unescaped_words == original_words, "Unescaping the escaped words should result in the original words"
        
def test_split_and_escape_then_unescape_and_join():
    examples = [
        "Resistivity is_commonly represented by the Greek letter ρ (rho).\n\nThe SI unit of electrical resistivity is the ohm-meter (Ω⋅m)."
    ]
    
    pre = PreTokenizer(alphabet=EU24_ALPHABET, normalization="ipt")
    for example in examples:
        words, ranges_before = pre.split_and_escape(example, return_ranges=True)
        text, ranges_after = pre.unescape_and_join(words, return_ranges=True)
        assert len(words) > 1, "Text should be split into multiple words"
        assert ranges_before == ranges_after, "The ranges should be the same before and after unescaping and joining"
        assert example == text, "Rejoining the unescaped words should result in the original text"

def test_split_and_escape_special():
    pre = PreTokenizer(alphabet=EU24_ALPHABET, normalization="ipt", reserved_tokens=["[RESERVED]"])
    example = "[RESERVED][RESERVED]Resistivity[RESERVED]is [RESERVED]"
    expected = ["[RESERVED]", "[RESERVED]", "Uresistivity", "[RESERVED]", "is", "G", "[RESERVED]"]
    words, ranges = pre.split_and_escape(example, return_ranges=True, handle_reserved=True)
    assert words == expected, f"Expected {expected}, got {words}"
