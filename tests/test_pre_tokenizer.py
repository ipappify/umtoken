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

def test_split_and_escape_ranges_fast_path_identity():
    """Pure ASCII text takes the fast path: ranges should index the input directly
    and reconstruct the original word-for-word."""
    pre = PreTokenizer(alphabet=EU24_ALPHABET, normalization="ipt")
    example = "Hello world foo bar baz"
    words, ranges = pre.split_and_escape(example, return_ranges=True)
    reconstructed = "".join(example[s:s+l] for s, l in ranges)
    assert reconstructed == example, f"ranges should reconstruct the original input; got {reconstructed!r}"
    for word, (s, l) in zip(words, ranges):
        assert pre.unescape(word) == example[s:s+l].lower() or pre.unescape(word) == example[s:s+l], \
            f"unescape({word!r}) should round-trip with original substring {example[s:s+l]!r}"

def test_split_and_escape_ranges_with_nfc_composition():
    """Decomposed input: 'Cafe' + combining acute. NFC composes it to 'Café' (5 source chars -> 4 normalized chars).
    The first range must still cover the *original* 5-char span, not the 4-char normalized one."""
    pre = PreTokenizer(alphabet=EU24_ALPHABET, normalization="default")
    example = "Café latte"  # 11 source chars; normalized is "Café latte" (10 chars)
    words, ranges = pre.split_and_escape(example, return_ranges=True)
    assert "".join(example[s:s+l] for s, l in ranges) == example, "ranges should partition the original decomposed text"
    # the first word's range must include the trailing combining mark
    first_start, first_len = ranges[0]
    assert example[first_start:first_start+first_len] == "Café", \
        f"first range should cover decomposed 'Cafe\\u0301'; got {example[first_start:first_start+first_len]!r}"

def test_split_and_escape_ranges_with_ipt_nfkc():
    """'ipt' mode NFKC: '²' -> '2'. Range for '2' must still point at the original '²' position."""
    pre = PreTokenizer(alphabet=EU24_ALPHABET, normalization="ipt")
    example = "x²+y³"
    words, ranges = pre.split_and_escape(example, return_ranges=True)
    assert "".join(example[s:s+l] for s, l in ranges) == example
    # find the word that unescapes to "2" — its range must point at the '²' in the original text
    for word, (s, l) in zip(words, ranges):
        if pre.unescape(word) == "2":
            assert example[s:s+l] == "²", f"range for normalized '2' should be the original '²'; got {example[s:s+l]!r}"
            break
    else:
        assert False, f"expected a word that unescapes to '2'; got {[pre.unescape(w) for w in words]}"

def test_split_and_escape_ranges_with_stripped_cf():
    """Format characters (zero-width space) get stripped by normalize. The ZWSP position must still be
    accounted for so that reconstruction from ranges yields the original text."""
    pre = PreTokenizer(alphabet=EU24_ALPHABET, normalization="default")
    example = "foo​bar baz"  # ZWSP is \p{Cf}, stripped; the rest is unchanged
    words, ranges = pre.split_and_escape(example, return_ranges=True)
    assert "".join(example[s:s+l] for s, l in ranges) == example, \
        "ranges should cover every original character, including stripped Cf"

def test_split_and_escape_ranges_with_reserved_and_unicode():
    """Reserved-token splitting must produce ranges in the *original* text even when
    surrounding text undergoes length-changing normalization."""
    pre = PreTokenizer(alphabet=EU24_ALPHABET, normalization="ipt", reserved_tokens=["[X]"])
    example = "ab[X]x²"  # mix of reserved token and 'ipt'-normalized '²'
    words, ranges = pre.split_and_escape(example, return_ranges=True, handle_reserved=True)
    assert "".join(example[s:s+l] for s, l in ranges) == example
    # the [X] reserved token must map to its original position
    for word, (s, l) in zip(words, ranges):
        if word == "[X]":
            assert example[s:s+l] == "[X]"
            break
    else:
        assert False, f"expected '[X]' among the words; got {words}"
