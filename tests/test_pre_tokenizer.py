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
        
def test_split_markup():
    pre = PreTokenizer(alphabet=EU24_ALPHABET, normalization="ipt")

    standalone_tokens = [
        "#", "##", "####",
        "=", "==", "====",
        "-", "--", "----",
        "+", "++", "++++",
        "/", "//", "////",
        "\\", "\\\\", "\\\\\\\\",
        "*", "**", "****",
        "~", "~~", "~~~~",
        "_", "__", "____",
        "<sup>", "</sup>",
        "<sub>", "</sub>",
        "<u>", "</u>",
        "{==", "==}",
        "{++", "++}",
        "{--", "--}",
    ]
    for token in standalone_tokens:
        words = pre.split(token)
        assert words == [token], f"Expected {[token]}, got {words}"

    embedded_examples = [
        ("x<sup>2</sup>+y", ["x", "<sup>", "2", "</sup>", "+", "y"]),
        ("H<sub>2</sub>O", ["H", "<sub>", "2", "</sub>", "O"]),
        ("foo<u>bar</u>", ["foo", "<u>", "bar", "</u>"]),
        ("text{++added++}more", ["text", "{++", "added", "++}", "more"]),
        ("text{--removed--}more", ["text", "{--", "removed", "--}", "more"]),
        ("text{==highlighted==}more", ["text", "{==", "highlighted", "==}", "more"]),
        ("a-b", ["a", "-", "b"]),
        ("word--word", ["word", "--", "word"]),
        ("<ux>", ["<", "ux", ">"]),
    ]
    for example, expected in embedded_examples:
        words = pre.split(example)
        assert words == expected, f"For {example!r}: expected {expected}, got {words}"
        assert example == "".join(words), f"Rejoining {example!r} should yield the original text"

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
        ("UNRESERVED", "YYunreserved"),
        ("RESERVED", "RESERVED"),
        ("火影", "UE7U81UABUE5UBDUB1"),
    ]
    pre = PreTokenizer(alphabet=EU24_ALPHABET, normalization="ipt", reserved_tokens=["RESERVED"])
    for example, expected in examples:
        actual = pre.escape(example, handle_reserved=True)
        assert actual == expected, f"Expected {expected}, got {pre.escape(example)}"

def test_escape_as_tupple():
    examples = [
        ("    ", ("GGGG", 0, 0)),
        ("\n\n", ("NN", 0, 0)),
        (" ws", ("ws", 1, 0)),
        ("UNRESERVED", ("unreserved", 0, 2)),
        ("RESERVED", ("RESERVED", 0, 0)),
        ("火影", ("UE7U81UABUE5UBDUB1", 0, 0)),
    ]
    pre = PreTokenizer(alphabet=EU24_ALPHABET, normalization="ipt", reserved_tokens=["RESERVED"])
    for example, expected in examples:
        actual = pre.escape(example, handle_reserved=True, return_as_tuple=True)
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
    expected = ["[RESERVED]", "[RESERVED]", "Yresistivity", "[RESERVED]", "is", "G", "[RESERVED]"]
    words, ranges = pre.split_and_escape(example, return_ranges=True, handle_reserved=True)
    assert words == expected, f"Expected {expected}, got {words}"
