# Path: umtoken/pre.py

from typing import List, Literal, Optional, Tuple, Union
import regex as re
import unicodedata

from .alphabet import Encoding, unescape
from .utils import cumsum

# default pre-split regex
# 1. match sequence of lowercase letters ("lower": sequence of any of Ll, Lo, Lm)
# 2. match sequence of uppercase letters followed by lowercase letters ("Camel": Lu Ll or Lt, optionally followed by sequence of any of Ll, Lo, Lm)
# 3. match sequence of uppercase letters not followed by lowercase letters ("UPPER": Lu Lu, optionally followed by sequence of any of Lu, Lo, Lm, not followed by Ll)
# 4. (Japanese/Chinese character sequences - removed to focus on European languages)
# 5. match sequence of digits ("123")
# 6. match (repeated) whitespace character - this may be useful for indentation in code or markdown
# 7. match any (repeated) character that is not a letter, digit, or whitespace
# wherein a single blank is merged to any succeeding match that is not a whitespace
SPLIT_REGEX = r'( ?(?:[\p{Ll}\p{Lo}\p{Lm}]+|(?:\p{Lu}\p{Ll}|\p{Lt})[\p{Ll}\p{Lo}\p{Lm}]*|\p{Lu}\p{Lu}[\p{Lu}\p{Lo}\p{Lm}]*(?!\p{Ll})|\d+|(?<! )(\s)\2*|(.)\3*))'

PAD_TOKEN = "[PAD]" # padding token
UNK_TOKEN = "[UNK]" # unknown token (should never happen because we escape all text - also used if something goes wrong in model.encode)
PRE_TOKEN = "[PRE]" # preambel token (e.g. for language or role identification: [PRE]assistant[SOT]<...>[EOT])
SOT_TOKEN = "[SOT]" # start of text token
EOT_TOKEN = "[EOT]" # end of text token
MSK_TOKEN = "[MSK]" # mask token
CLS_TOKEN = "[CLS]" # classification token
FEED_TOKEN = "[FEED]" # feed token
EMIT_TOKEN = "[EMIT]" # emit token
CUR_TOKEN = "[CUR]" # cursor token

DEFAULT_RESERVED_TOKENS = [PAD_TOKEN, UNK_TOKEN, PRE_TOKEN, SOT_TOKEN, EOT_TOKEN,
                           MSK_TOKEN, CLS_TOKEN, FEED_TOKEN, EMIT_TOKEN, CUR_TOKEN]

_ws_or_control_regex = re.compile(r'\p{Z}(?<! )|\p{Cc}(?<![\t\n])', re.UNICODE)
_alpha_or_num_regex = re.compile(r'\p{N}|(\p{L}(?<!\p{Lm}))+', re.UNICODE)

class PreTokenizer:
    def __init__(self, 
                 alphabet: Optional[str] = None, 
                 encoding: Optional[Encoding] = None,
                 normalization: Optional[Literal["default", "ipt", "nfc"]] = "default",
                 split_regex=SPLIT_REGEX,
                 reserved_tokens: List[str] = DEFAULT_RESERVED_TOKENS,
                 preserve_soft_hyphen: bool = False,
                 preserve_format_and_diactritic: bool = False):
        """
        Pre-tokenizer that pre-splits and optionally encodes (escapes) the text.
        
        Args:
            alphabet: The alphabet to encode the words with (cannot be provided together with encoding).
            encoding: The encoding to use (cannot be provided together with alphabet).
            normalization: The normalization to apply to the text before escaping it.
                           'default': normalize the text to NFC and remove control characters, format characters, and uncombined diacritics
                           'ipt': additionally normalize digits and letters to NFKC (² -> 2, 𝑀 -> M, etc.) - 
                                  this is useful if formatting (superscipt, math italic, etc.) is handled on application level (as in IP.Translator)
                           'nfc': normalize the text to NFC only
                           None: do not normalize the text
            split_regex: The regex to pre-split the text. Only the first matched group (group 1) is returned.
            reserved_tokens: The list of reserved tokens (words) which should not be split and escaped.
            preserve_soft_hyphen: Whether to preserve the soft hyphen character (U+00AD) before splitting.
            preserve_format_and_diactritic: Whether to preserve format characters (Cf) and uncombined diacritics (M) before splitting.
            
        Remarks:
            The term word is used here to refer to split units of text (including punctuation, whitespace, etc.)
            to avoid confusion with (subword) tokens returned by the tokenizer.
            In the case of reserved tokens, "words" and "tokens" should be the same, because the tokenizer should not split them.
            
            The pre-tokenizer converts uppercase letters to lowercase during escape and restores the case during unescape.
            However, there are some uppercase Unicode characters that have the same lowercase representation (e.g. "Å" (Ångstrom) and "Å" (Latin capital A with a ring above)).
            In such cases, certain original uppercase characters (e.g., "Å" (Ångstrom)) cannot be recovered.
            If it is important to preserve the original character, the PreTokenizer must be modified to exclude such characters from case conversion.
            Similar considerations apply to the Turkish dotted "I" and dotless "i".
        """
        
        assert alphabet is None or encoding is None, "alphabet and encoding must not be provided simultaneously"
        assert normalization is None or normalization in ["default", "ipt", "nfc"], "normalization must be None, 'ipt', or 'nfc'"
        
        self.encoding = encoding or (Encoding(alphabet) if alphabet is not None else None)
        self.normalization = normalization
        self.split_regex = re.compile(split_regex, re.UNICODE)
        self.reserved_tokens = frozenset(reserved_tokens or [])
        self.reserved_tokens_regex = re.compile("(" + "|".join(re.escape(t) for t in self.reserved_tokens) + ")", re.UNICODE) if reserved_tokens else None
        self.preserve_soft_hyphen = preserve_soft_hyphen
        self.preserve_format_and_diactritic = preserve_format_and_diactritic
        
        if not preserve_format_and_diactritic:
            if not preserve_soft_hyphen:
                self._clean_regex = re.compile(r'\p{Cf}|\p{M}', re.UNICODE)
            else:
                self._clean_regex = re.compile(r'\p{Cf}(?<!\u00AD)|\p{M}', re.UNICODE)
        else:
            if not preserve_soft_hyphen:
                self._clean_regex = re.compile(r'\u00AD', re.UNICODE)
            else:
                self._clean_regex = None            
    
    def split(self, text: str, handle_reserved: bool = False, allowed_reserved: Optional[list[str]] = None) -> List[str]:
        """
        Splits the text into words.
        
        Args:
            text: The text to split.
            handle_reserved: Whether to handle reserved tokens. If True, reserved tokens are not split and escaped.
            allowed_reserved: Restrict allowed reserved tokens to this list, if provided.
            
        Returns:
            The list of words.
        """
        assert text is None or isinstance(text, str), f"Expected string for text, got {type(text)}"
        if text is None or len(text) == 0:
            return []
        
        text = self.normalize(text)
        
        if handle_reserved and self.reserved_tokens:
            reserved_tokens_regex = self.reserved_tokens_regex
            if allowed_reserved:
                reserved_tokens_regex = re.compile("(" + "|".join(re.escape(t) for t in allowed_reserved) + ")", re.UNICODE)
            parts = reserved_tokens_regex.split(text)
            words = []
            for i, part in enumerate(parts):
                if i % 2 == 0:
                    if part:
                        words.extend(self.split(part))
                else:
                    words.append(part)
            return words
        else:
            return list(m.group(1) for m in self.split_regex.finditer(text))
        
    def normalize(self, text: str) -> str:
        if self.normalization in ["default", "ipt", "nfc"]:
            text = unicodedata.normalize("NFC", text)

        if self.normalization in ["default", "ipt"]:
            # replace non-standard whitespaces and controls with blank space
            text = _ws_or_control_regex.sub(" ", text)

        if self.normalization == "ipt":
            # normalize digits and letters to NFKC
            # ² -> 2, 𝑀 -> M, etc.
            text = _alpha_or_num_regex.sub(lambda w: unicodedata.normalize("NFKC", w.group(0)), text)
            
        if self._clean_regex:
            text = self._clean_regex.sub("", text)

        return text
        
    def escape(self, 
               word: str, 
               handle_reserved: bool = False, 
               allowed_reserved: Optional[list[str]] = None,
               return_as_tuple: bool = False) -> str:
        """
        Escapes the word.
        
        Args:
            word: The word to escape.
            handle_reserved: Whether to handle reserved tokens. If True, reserved tokens are not escaped.
            allowed_reserved: Restrict allowed reserved tokens to this list, if provided.
            return_as_tuple: Whether to return the escaped word as a tuple (escaped word, whitespace, uppercase).
            
        Returns:
            The escaped word.
        """
        assert self.encoding is not None, "Encoding must be provided to escape words"
        
        if word is None or len(word) == 0:
            return word if not return_as_tuple else (word, 0, 0)

        if handle_reserved and self.reserved_tokens:
            if word in self.reserved_tokens and (allowed_reserved is None or word in allowed_reserved):
                return word if not return_as_tuple else (word, 0, 0)
        
        return self.encoding.escape(word, return_as_tuple)
        
    def split_and_escape(self, text: str, 
                         handle_reserved: bool = False,
                         allowed_reserved: Optional[list[str]] = None,
                         return_ranges: bool = False,
                         return_as_tuple: bool = False) -> Union[List[str], Tuple[List[str], List[Tuple[int, int]]]]:
        """
        Splits the text into words, normalizes, and escapes them.
        
        Args:
            text: The text to split and escape.
            handle_reserved: Whether to handle reserved tokens. If True, reserved tokens are not split and escaped.
            allowed_reserved: Restrict allowed reserved tokens to this list, if provided.
            return_ranges: Whether to return the ranges of the original words (offset, length) in the text (before they are normalized and escaped).
            return_as_tuple: Whether to return the escaped words as tuples (escaped word, whitespace, uppercase).
            
        Returns:
            If return_ranges is False, the list of escaped words.
            If return_ranges is True, the list of escaped words and the list of ranges of the original words in the text.
        """
        if not self.preserve_soft_hyphen:
            text = text.replace("\u00AD", "")
        
        words = self.split(text, handle_reserved, allowed_reserved)
        if return_ranges:
            idxs = cumsum(len(w) for w in words)
            ranges = [(start, len(word)) for word, start in zip(words, idxs)]
        words = [self.escape(word, 
                             handle_reserved=handle_reserved, 
                             allowed_reserved=allowed_reserved, 
                             return_as_tuple=return_as_tuple) for word in words]
        return (words, ranges) if return_ranges else words
    
    def unescape(self, 
                 escaped: Union[str, Tuple[str,int,int]],
                 handle_reserved: bool = False,) -> str:
        """
        Unescapes the escaped word.
        
        Args:
            escaped: The escaped word to unescape.
            handle_reserved: Whether to handle reserved tokens. If True, reserved tokens are not unescaped.
            
        Returns:
            The unescaped word.
        """
        if handle_reserved:
            if isinstance(escaped, tuple):
                if escaped[0] in self.reserved_tokens:
                    return escaped[0] 
            elif escaped in self.reserved_tokens:
                return escaped
        return unescape(escaped)
    
    def unescape_and_join(self, words: List[str], omit_reserved: bool = True, 
                          return_ranges: bool = False) -> Union[str, Tuple[str, List[Tuple[int, int]]]]:
        """
        Unescapes the words and joins them into a single string.
        
        Args:
            words: The list of words to unescape and join.
            omit_reserved: Whether to omit reserved tokens from the joined text.
            return_ranges: Whether to return the ranges of the original words (offset, length) in the text (before they are unescaped).
            
        Returns:
            The unescaped and joined text.
        """
        words = iter(self.unescape(word) for word in words)
        if omit_reserved:
            words = iter((word if word not in self.reserved_tokens else "") for word in words)
            
        if return_ranges:
            words = list(words)
            idxs = cumsum(len(w) for w in words)
            ranges = [(start, len(word)) for word, start in zip(words, idxs)]
            
        text = "".join(words)
        return (text, ranges) if return_ranges else text
    
    def save_dict(self) -> dict:
        return {
            "alphabet": self.encoding.alphabet,
            "normalization": self.normalization,
            "split_regex": self.split_regex.pattern,
            "reserved_tokens": list(self.reserved_tokens),
            "preserve_soft_hyphen": self.preserve_soft_hyphen
        }
    
    @staticmethod
    def load_dict(d: dict):
        return PreTokenizer(
            alphabet=d.get("alphabet"),
            normalization=d.get("normalization"),
            split_regex=d.get("split_regex"),
            reserved_tokens=d.get("reserved_tokens"),
            preserve_soft_hyphen=d.get("preserve_soft_hyphen")
        )
        