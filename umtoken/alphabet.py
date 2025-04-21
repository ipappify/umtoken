# Path: umtoken/alphabet.py

import warnings
from typing import List, Tuple, Union
import regex as re

# do not include uppercase letters - the pre-tokenizer normalizes all text to lowercase
MIN_LATIN_ALPHABET = "abcdefghijklmnopqrstuvwxyz"
MIN_CYRILLIC_ALPHABET = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
MIN_GREEK_ALPHABET = "αβγδεζηθικλμνξοπρστυφχψω"

# do not include letters - they are already included in the basic latin alphabet
# blank, tab, newline, and soft-hyphen will be escaped (as G, T, N, H, respectively)
ASCII_DIGITS = "0123456789"
ASCII_PUNCTUATION = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"

# uppercase characters are used for escape sequences
ASCII_RESERVED_EOW = "X"       # end of word - not used in encoding, but reserved for model to indicate end of word
ASCII_RESERVED_UPPER = "Y"     # upper case (Y for title, YY for upper case) - only used for formatting pre-tokenized text
ASCII_RESERVED_UTF8 = "U"      # prefix for utf-8 encoded bytes - should not be used alone 
ASCII_RESERVED_HEX = "ABCDEF"  # hex digits for utf-8 encoded bytes - should not be used alone
ASCII_ENCODING_SPACE = "G"   # in pre-tokenized format, spaces are replaced by this token
ASCII_ENCODING_SHY = "H"     # in pre-tokenized format, soft-hyphens are replaced by this token
ASCII_ENCODING_NEWLINE = "N" # in pre-tokenized format, newlines are replaced by this token
ASCII_ENCODING_TAB = "T"     # in pre-tokenized format, tabs are replaced by this token
ASCII_ENCODING = "".join([ASCII_ENCODING_SPACE, ASCII_ENCODING_SHY, ASCII_ENCODING_NEWLINE, ASCII_ENCODING_TAB])
ASCII_ALL = "".join([ASCII_ENCODING, ASCII_DIGITS, ASCII_PUNCTUATION])

# 24 EU official languages
EXT_CYRILLIC_BG = "йцъ" # Bulgarian
EXT_LATIN_HR = "čćžđš" # Croatian
EXT_LATIN_CS = "áčďéěíňóřšťúůýž" # Czech
EXT_LATIN_DA = "æøå" # Danish
EXT_LATIN_NL = "ëéèïí" # Dutch
EXT_LATIN_EN = "" # English
EXT_LATIN_ET = "äõöüšž" # Estonian
EXT_LATIN_FI = "åäö" # Finnish
EXT_LATIN_FR = "àâæçéèêëîïôœùûüÿ" # French
EXT_LATIN_DE = "äöüß" # German
EXT_GREEK_EL = "άέήίύώόϊϋΐΰς" # Greek
EXT_LATIN_HU = "áéíóöőúüű" # Hungarian
EXT_LATIN_GA = "áéíóú" # Irish
EXT_LATIN_IT = "àèéìíîòóùú" # Italian
EXT_LATIN_LV = "āčēģīķļņšūž" # Latvian
EXT_LATIN_LT = "ąčęėįšųūž" # Lithuanian
EXT_LATIN_MT = "ċġħiż" # Maltese
EXT_LATIN_PL = "ąćęłńóśźż" # Polish
EXT_LATIN_PT = "áâãàçéêíóôõú" # Portuguese
EXT_LATIN_RO = "âîășț" # Romanian
EXT_LATIN_SK = "áäčďéíĺľňóôŕšťúýž" # Slovak
EXT_LATIN_SL = "čšž" # Slovenian
EXT_LATIN_ES = "áéíñóúü" # Spanish
EXT_LATIN_SV = "åäö" # Swedish

# EEA official languages
EXT_LATIN_NO = "æøå" # Norwegian
EXT_LATIN_IS = "áðéíóúýæö" # Icelandic

# Other languages
EXT_CYRILLIC_RU = "йцъы" # Russian
EXT_LATIN_TR = "çğıöşü" # Turkish

# Additional punctuation
EXT_PUNCTUATION = "’»«›‹„“”·¡¿…–—‐†‡§"

MIN_ALPHABET = ASCII_ALL + EXT_PUNCTUATION + MIN_LATIN_ALPHABET
EU3_ALPHABET = ASCII_ALL + EXT_PUNCTUATION + "".join(sorted(set(MIN_LATIN_ALPHABET + EXT_LATIN_EN + EXT_LATIN_FR + EXT_LATIN_DE)))
EU5_ALPHABET = ASCII_ALL + EXT_PUNCTUATION + "".join(sorted(set(MIN_LATIN_ALPHABET + EXT_LATIN_EN + EXT_LATIN_FR + EXT_LATIN_DE + EXT_LATIN_IT + EXT_LATIN_ES)))
EU24_ALPHABET = ASCII_ALL + EXT_PUNCTUATION + "".join(sorted(set(MIN_LATIN_ALPHABET + MIN_CYRILLIC_ALPHABET + MIN_GREEK_ALPHABET + 
                                                                 EXT_CYRILLIC_BG + EXT_LATIN_HR + EXT_LATIN_CS + EXT_LATIN_DA + 
                                                                 EXT_LATIN_NL + EXT_LATIN_EN + EXT_LATIN_ET + EXT_LATIN_FI + 
                                                                 EXT_LATIN_FR + EXT_LATIN_DE + EXT_GREEK_EL + EXT_LATIN_HU + 
                                                                 EXT_LATIN_GA + EXT_LATIN_IT + EXT_LATIN_LV + EXT_LATIN_LT + 
                                                                 EXT_LATIN_MT + EXT_LATIN_PL + EXT_LATIN_PT + EXT_LATIN_RO + 
                                                                 EXT_LATIN_SK + EXT_LATIN_SL + EXT_LATIN_ES + EXT_LATIN_SV)))

LANG_TO_ALPHABET = {
    "bg": MIN_CYRILLIC_ALPHABET + EXT_CYRILLIC_BG,
    "hr": EXT_LATIN_HR,
    "cs": EXT_LATIN_CS,
    "da": EXT_LATIN_DA,
    "nl": EXT_LATIN_NL,
    "en": EXT_LATIN_EN,
    "et": EXT_LATIN_ET,
    "fi": EXT_LATIN_FI,
    "fr": EXT_LATIN_FR,
    "de": EXT_LATIN_DE,
    "el": MIN_GREEK_ALPHABET + EXT_GREEK_EL,
    "hu": EXT_LATIN_HU,
    "ga": EXT_LATIN_GA,
    "it": EXT_LATIN_IT,
    "lv": EXT_LATIN_LV,
    "lt": EXT_LATIN_LT,
    "mt": EXT_LATIN_MT,
    "pl": EXT_LATIN_PL,
    "pt": EXT_LATIN_PT,
    "ro": EXT_LATIN_RO,
    "sk": EXT_LATIN_SK,
    "sl": EXT_LATIN_SL,
    "es": EXT_LATIN_ES,
    "sv": EXT_LATIN_SV,
    "no": EXT_LATIN_NO,
    "is": EXT_LATIN_IS,
    "ru": MIN_CYRILLIC_ALPHABET + EXT_CYRILLIC_RU,
    "tr": EXT_LATIN_TR
}

def get_alphabet(languages: List[str]):
    """
    Returns the alphabet for a list of languages.
    
    Args:
        languages: A list of languages.
        
    Returns:
        The alphabet for the languages.
    """
    alphabet = MIN_LATIN_ALPHABET
    for lang in languages:
        lang_alphabet = LANG_TO_ALPHABET.get(lang, None)
        if lang_alphabet is not None:
            alphabet += lang_alphabet
        else:
            warnings.warn(f"No alphabet defined for language {lang}.")
    return ASCII_ALL + EXT_PUNCTUATION + "".join(sorted(set(alphabet)))    

def _escape_char(c: str) -> str:
    if c == " ":
        return ASCII_ENCODING_SPACE
    elif c == "\n":
        return ASCII_ENCODING_NEWLINE
    elif c == "\t":
        return ASCII_ENCODING_TAB
    elif c == "\u00AD":
        return ASCII_ENCODING_SHY
    else:
        bts = c.encode("utf-8")
        return "".join(ASCII_RESERVED_UTF8 + bts[i:i+1].hex().upper() for i in range(len(bts)))

def _unescape_char(c: str) -> str:
    if c == ASCII_ENCODING_SPACE:
        return " "
    elif c == ASCII_ENCODING_NEWLINE:
        return "\n"
    elif c == ASCII_ENCODING_TAB:
        return "\t"
    elif c[0] == ASCII_RESERVED_UTF8:
        try:
            c = c.replace(ASCII_RESERVED_UTF8, "")
            return bytes.fromhex(c).decode("utf-8")
        except:
            return "?"
    return "?"

_unescape_char_regex = re.compile(f"((?:{ASCII_RESERVED_UTF8}[0-9A-F]{{2}})+|[{ASCII_ENCODING_SPACE}{ASCII_ENCODING_NEWLINE}{ASCII_ENCODING_TAB}])")
def _unescape_chars(cs: str) -> str:
    return _unescape_char_regex.sub(lambda m: _unescape_char(m.group(1)), cs)

def unescape(escaped: Union[str, Tuple[str, int, int]]) -> str:
    """
    Unescapes an esacped word.
    
    Args:
        escaped: The escaped word.
        
    Returns:
        The unescaped word.
    """
    
    if escaped is None:
        return None
        
    if isinstance(escaped, tuple):
        word, ws, up = escaped
    else:
        if len(escaped) == 0:
            return ""
        elif escaped == ASCII_ENCODING_SPACE:
            return " "
        word = escaped
        ws = 0
        up = 0
        if word[0] == ASCII_ENCODING_SPACE:
            ws = 1
            word = word[1:]
        if word[0] == ASCII_RESERVED_UPPER:
            up = 2 if len(word) > 1 and word[1] == ASCII_RESERVED_UPPER else 1
            word = word[up:]
            
    word = _unescape_chars(word)
    if up == 1:
        word = word.capitalize()
    elif up == 2:
        word = word.upper()
    return ws * " " + word

class Encoding():
    def __init__(self, alphabet):
        """
        Encodes and decodes text using a custom alphabet.
        
        Args:
            alphabet: The alphabet to use for encoding and decoding.
        """
        self.alphabet = alphabet
        self.alphabet_set = frozenset(alphabet)
        self.alphabet_missing_regex = re.compile(f"[^{re.escape(alphabet)}]")
        
    def escape(self, word: str, return_as_tuple: bool = False) -> Union[str, Tuple[str, int, int]]:
        """
        Escape a word using the custom alphabet.
        
        Args:
            word: The word to encode.
            return_as_tuple: Whether to return the encoded word as a tuple (encoded word, whitespace, uppercase).
            
        Returns:
            The escaped word either as a formatted string or as a tuple. 
        """
        if not word:
            return "" if not return_as_tuple else ("", 0, 0)
        if word == " ":
            return ASCII_ENCODING_SPACE if not return_as_tuple else (ASCII_ENCODING_SPACE, 0, 0)
        
        ws = 0
        up = 0
        if word[0] == " " and word[1] != " ":
            ws = 1
            word = word[1:]
        if word[0].isupper():
            up = 2 if len(word) > 1 and word[1].isupper() else 1
        word = word.lower() # lower always to safeguard against errors when splitting before uppercase letters
        escaped = self._escape(word)
        if return_as_tuple:
            return escaped, ws, up
        else:
            return ws * ASCII_ENCODING_SPACE + up * ASCII_RESERVED_UPPER + escaped
        
    def _escape(self, word):
        return self.alphabet_missing_regex.sub(lambda m: _escape_char(m.group(0)), word)
    
    def unescape(self, escaped: Union[str, Tuple[str, int, int]]) -> str:
        """ Unescapes an escaped word. See global unescape for more information. """
        return unescape(escaped)    
