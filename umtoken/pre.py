# Path: umtoken/pre.py

from typing import Callable, Iterable, List, Literal, Optional, Tuple, Union
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
# 7. match sub/superscript/underline HTML tags as a single unit ("<sub>", "</sub>", "<sup>", "</sup>", "<u>", "</u>")
# 8. match CriticMarkup-style brackets as a single unit ("{==", "==}", "{++", "++}", "{--", "--}")
# 9. match any (repeated) character that is not a letter, digit, or whitespace
# wherein a single blank is merged to any succeeding match that is not a whitespace
SPLIT_REGEX = r'( ?(?:[\p{Ll}\p{Lo}\p{Lm}]+|(?:\p{Lu}\p{Ll}|\p{Lt})[\p{Ll}\p{Lo}\p{Lm}]*|\p{Lu}\p{Lu}[\p{Lu}\p{Lo}\p{Lm}]*(?!\p{Ll})|\d+|(?<! )(\s)\2*|</?(?:su[bp]|u)>|\{(?:==|\+\+|--)|(?:==|\+\+|--)\}|(.)\3*))'

PAD_TOKEN = "[PAD]" # padding token
UNK_TOKEN = "[UNK]" # unknown token (should never happen because we escape all text - also used if something goes wrong in model.encode)
SOT_TOKEN = "[SOT]" # start of text token
EOT_TOKEN = "[EOT]" # end of text token
MSK_TOKEN = "[MSK]" # mask token
CLS_TOKEN = "[CLS]" # classification token
RSV_TOKEN = "[RSV{i:03d}]" # reserved tokens


DEFAULT_RESERVED_TOKENS = ([PAD_TOKEN, UNK_TOKEN, SOT_TOKEN, EOT_TOKEN, MSK_TOKEN, CLS_TOKEN] + 
                           [f"{RSV_TOKEN.format(i=i)}" for i in range(26)])

_ws_or_control_regex = re.compile(r'\p{Z}(?<! )|\p{Cc}(?<![\t\n])', re.UNICODE)
_alpha_or_num_regex = re.compile(r'\p{N}|(\p{L}(?<!\p{Lm}))+', re.UNICODE)
# per-char form of _alpha_or_num_regex for the offset-tracking slow path
_alpha_or_num_char_regex = re.compile(r'\p{N}|[\p{Ll}\p{Lu}\p{Lt}\p{Lo}]', re.UNICODE)
# fast path for normalize(return_offsets=True): ASCII printable + tab/newline/CR + Latin-1 letter half
# every char in this set is NFC-stable, NFKC-stable, and not in \p{Cf}/\p{M}/\p{Cc}/non-space \p{Z}.
_norm_stable_regex = re.compile(r'\A[\x20-\x7E\t\n\rÀ-ÿ]*\Z', re.UNICODE)

class PreTokenizer:
    def __init__(self,
                 alphabet: Optional[str] = None,
                 encoding: Optional[Encoding] = None,
                 normalization: Optional[Literal["default", "ipt", "nfc"]] = "default",
                 split_regex=SPLIT_REGEX,
                 reserved_tokens: Optional[List[str]] = None,
                 preserve_soft_hyphen: Union[bool, str] = False,
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
            preserve_soft_hyphen: Whether to preserve the soft hyphen character (U+00AD).
                                  False or 'remove': remove soft hyphen
                                  True or 'preserve': preserve soft hyphen as isolated character and escape it
                                  'append': preserve soft hyphen and append it to the preceding word if any (otherwise preserve as isolated character)
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
        assert normalization is None or normalization in ["default", "ipt", "nfc"], "normalization must be None, 'default', 'ipt', or 'nfc'"
        assert preserve_soft_hyphen in [False, True, 'remove', 'preserve', 'append'], "preserve_soft_hyphen must be a boolean or one of 'remove', 'preserve', 'append'"

        if preserve_soft_hyphen == False:
            preserve_soft_hyphen = 'remove'
        elif preserve_soft_hyphen == True:
            preserve_soft_hyphen = 'preserve'

        if reserved_tokens is None:
            reserved_tokens = DEFAULT_RESERVED_TOKENS
        # keep an ordered, deduped list so the alternation regex is deterministic across runs;
        # longest-first so a shorter token can't shadow a longer one with the same prefix.
        seen = set()
        self.reserved_tokens_list = [t for t in reserved_tokens if not (t in seen or seen.add(t))]
        regex_order = sorted(self.reserved_tokens_list, key=len, reverse=True)

        self.encoding = encoding or (Encoding(alphabet) if alphabet is not None else None)
        self.normalization = normalization
        self.split_regex = re.compile(split_regex, re.UNICODE)
        self.reserved_tokens = frozenset(self.reserved_tokens_list)
        self.reserved_tokens_regex = re.compile("(" + "|".join(re.escape(t) for t in regex_order) + ")", re.UNICODE) if regex_order else None
        self._allowed_reserved_regex_cache = {}
        self.preserve_soft_hyphen = preserve_soft_hyphen
        self.preserve_format_and_diactritic = preserve_format_and_diactritic
        
        if not preserve_format_and_diactritic:
            if preserve_soft_hyphen == 'remove':
                self._clean_regex = re.compile(r'\p{Cf}|\p{M}', re.UNICODE)
            else:
                self._clean_regex = re.compile(r'\p{Cf}(?<!\u00AD)|\p{M}', re.UNICODE)
        else:
            if preserve_soft_hyphen == 'remove':
                self._clean_regex = re.compile(r'\u00AD', re.UNICODE)
            else:
                self._clean_regex = None            
    
    def split(self, text: str, 
              handle_reserved: bool = False, allowed_reserved: Optional[list[str]] = None,
              split_compound_func: Optional[Callable] = None) -> List[str]:
        """
        Splits the text into words.
        
        Args:
            text: The text to split.
            handle_reserved: Whether to handle reserved tokens. If True, reserved tokens are not split and escaped.
            allowed_reserved: Restrict allowed reserved tokens to this list, if provided.
            split_compound_func: Callable that splits a word into one or more parts (str->list[str]).
                                 The callable is responsible for maintaining case and appending soft hyphens to mods if necessary.   
            
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
                key = frozenset(allowed_reserved)
                reserved_tokens_regex = self._allowed_reserved_regex_cache.get(key)
                if reserved_tokens_regex is None:
                    # longest-first, same as the main regex, to keep matching deterministic and prefix-safe
                    ordered = sorted(set(allowed_reserved), key=len, reverse=True)
                    reserved_tokens_regex = re.compile("(" + "|".join(re.escape(t) for t in ordered) + ")", re.UNICODE)
                    self._allowed_reserved_regex_cache[key] = reserved_tokens_regex
            parts = reserved_tokens_regex.split(text)
            words = []
            for i, part in enumerate(parts):
                if i % 2 == 0:
                    if part:
                        words.extend(self.split(part))
                else:
                    words.append(part)
        else:
            words = list(m.group(1) for m in self.split_regex.finditer(text))
            
        if self.preserve_soft_hyphen == 'append' and any(w == "\u00AD" for w in words):
            # append soft hyphen to preceding word if any
            new_words = []
            for i, w in enumerate(words):
                if w == "\u00AD" and i > 0 and not words[i-1].endswith("\u00AD"):
                    new_words[-1] += w
                else:
                    new_words.append(w)
            words = new_words

        # split compound words into parts; reserved tokens are never split
        if split_compound_func is not None:
            reserved = self.reserved_tokens if handle_reserved else frozenset()
            split_words = []
            for w in words:
                if w in reserved:
                    split_words.append(w)
                else:
                    split_words.extend(split_compound_func(w))
            words = split_words

        return words
        
    def normalize(self, text: str, return_offsets: bool = False):
        """Normalize text. If ``return_offsets`` is False, returns the normalized string.
        If True, returns a tuple ``(normalized, src_map)`` where ``src_map[i]`` is the
        index in the original ``text`` corresponding to the i-th character of the
        normalized output, plus a sentinel ``src_map[len(normalized)] == len(text)``.
        ``src_map`` is ``None`` when normalization was an identity (fast path)."""
        if not return_offsets:
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

        # offset-aware path
        if _norm_stable_regex.match(text):
            return text, None
        return self._normalize_with_offsets(text)

    def _normalize_with_offsets(self, text: str):
        """Slow path of ``normalize`` that produces an offset map alongside the
        normalized text. Each output character is tagged with the index of the
        first source character it came from; a sentinel equal to ``len(text)`` is
        appended so end-positions can be looked up uniformly.

        Caveat: NFC is applied per canonical combining sequence (starter + marks),
        so fully-decomposed Hangul jamo sequences (L+V+T as separate codepoints)
        will not recompose here. Real-world Hangul is overwhelmingly pre-composed,
        which is NFC-stable and unaffected."""
        n = len(text)
        chars: List[str] = []
        src: List[int] = []

        if self.normalization in ["default", "ipt", "nfc"]:
            i = 0
            while i < n:
                j = i + 1
                while j < n and unicodedata.combining(text[j]) != 0:
                    j += 1
                for c in unicodedata.normalize("NFC", text[i:j]):
                    chars.append(c)
                    src.append(i)
                i = j
        else:
            chars = list(text)
            src = list(range(n))

        if self.normalization in ["default", "ipt"]:
            for k in range(len(chars)):
                if _ws_or_control_regex.match(chars[k]):
                    chars[k] = " "

        if self.normalization == "ipt":
            new_chars: List[str] = []
            new_src: List[int] = []
            for c, s in zip(chars, src):
                if _alpha_or_num_char_regex.match(c):
                    for nc in unicodedata.normalize("NFKC", c):
                        new_chars.append(nc)
                        new_src.append(s)
                else:
                    new_chars.append(c)
                    new_src.append(s)
            chars, src = new_chars, new_src

        if self._clean_regex is not None:
            out_chars: List[str] = []
            out_src: List[int] = []
            for c, s in zip(chars, src):
                if not self._clean_regex.match(c):
                    out_chars.append(c)
                    out_src.append(s)
            chars, src = out_chars, out_src

        src.append(n)
        return "".join(chars), src
        
    def escape(self,
               word: str,
               handle_reserved: bool = False,
               allowed_reserved: Optional[list[str]] = None,
               return_as_tuple: bool = False) -> Union[str, Tuple[str, int, int]]:
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
                         return_as_tuple: bool = False,
                         split_compound_func: Optional[Callable] = None) -> Union[List[str], Tuple[List[str], List[Tuple[int, int]]]]:
        """
        Splits the text into words, normalizes, and escapes them.

        Args:
            text: The text to split and escape.
            handle_reserved: Whether to handle reserved tokens. If True, reserved tokens are not split and escaped.
            allowed_reserved: Restrict allowed reserved tokens to this list, if provided.
            return_ranges: Whether to return the ranges (offset, length) of each word as positions in the *original* text (before normalization and escaping).
            return_as_tuple: Whether to return the escaped words as tuples (escaped word, whitespace, uppercase).
            split_compound_func: Callable that splits a word into one or more parts (str->list[str]).
                                 The callable is responsible for maintaining case and appending soft hyphens to mods if necessary.
                                 When return_ranges is True, each part's range is derived from the original word's span.

        Returns:
            If return_ranges is False, the list of escaped words.
            If return_ranges is True, a tuple (escaped words, ranges in the original text).
        """
        # SHY removal in 'remove' mode is handled by normalize() inside split(); no need to pre-strip here.
        if not return_ranges:
            words = self.split(text, handle_reserved, allowed_reserved, split_compound_func=split_compound_func)
            words = [self.escape(word,
                                 handle_reserved=handle_reserved,
                                 allowed_reserved=allowed_reserved,
                                 return_as_tuple=return_as_tuple) for word in words]
            return words

        # Range-tracking path: normalize once with offsets, then split the normalized text
        # directly so match positions can be mapped back into the original text.
        if text is None or len(text) == 0:
            return [], []

        normalized, src_map = self.normalize(text, return_offsets=True)

        def to_orig(n_start: int, n_end: int) -> Tuple[int, int]:
            if src_map is None:
                return (n_start, n_end - n_start)
            return (src_map[n_start], src_map[n_end] - src_map[n_start])

        word_spans = list(self._split_normalized(normalized, handle_reserved, allowed_reserved))

        if self.preserve_soft_hyphen == 'append' and any(w == "­" for w, _, _ in word_spans):
            merged: List[Tuple[str, int, int]] = []
            for w, ns, ne in word_spans:
                if w == "­" and merged and not merged[-1][0].endswith("­"):
                    pw, pns, _ = merged[-1]
                    merged[-1] = (pw + w, pns, ne)
                else:
                    merged.append((w, ns, ne))
            word_spans = merged

        # split compound words into parts, partitioning each word's normalized
        # span among the parts; reserved tokens are never split
        if split_compound_func is not None:
            reserved = self.reserved_tokens if handle_reserved else frozenset()
            split_spans: List[Tuple[str, int, int]] = []
            for w, ns, ne in word_spans:
                if w in reserved:
                    split_spans.append((w, ns, ne))
                else:
                    split_spans.extend(self._assign_compound_ranges(split_compound_func(w), w, ns, ne))
            word_spans = split_spans

        escaped = [self.escape(w,
                               handle_reserved=handle_reserved,
                               allowed_reserved=allowed_reserved,
                               return_as_tuple=return_as_tuple) for w, _, _ in word_spans]
        ranges = [to_orig(ns, ne) for _, ns, ne in word_spans]
        return escaped, ranges

    def _split_normalized(self, text: str,
                          handle_reserved: bool,
                          allowed_reserved: Optional[List[str]]) -> Iterable[Tuple[str, int, int]]:
        """Split already-normalized text, yielding (word, start, end) with positions
        in the normalized text. Mirrors the splitting logic of :meth:`split` but
        does not re-normalize and exposes match positions."""
        if handle_reserved and self.reserved_tokens:
            reserved_regex = self.reserved_tokens_regex
            if allowed_reserved:
                key = frozenset(allowed_reserved)
                reserved_regex = self._allowed_reserved_regex_cache.get(key)
                if reserved_regex is None:
                    ordered = sorted(set(allowed_reserved), key=len, reverse=True)
                    reserved_regex = re.compile("(" + "|".join(re.escape(t) for t in ordered) + ")", re.UNICODE)
                    self._allowed_reserved_regex_cache[key] = reserved_regex
            pos = 0
            for rm in reserved_regex.finditer(text):
                if pos < rm.start():
                    for sm in self.split_regex.finditer(text, pos, rm.start()):
                        yield sm.group(1), sm.start(1), sm.end(1)
                yield rm.group(0), rm.start(), rm.end()
                pos = rm.end()
            if pos < len(text):
                for sm in self.split_regex.finditer(text, pos):
                    yield sm.group(1), sm.start(1), sm.end(1)
        else:
            for sm in self.split_regex.finditer(text):
                yield sm.group(1), sm.start(1), sm.end(1)

    def _assign_compound_ranges(self, parts: List[str], word: str,
                                ns: int, ne: int) -> List[Tuple[str, int, int]]:
        """Partition the normalized span ``[ns, ne)`` of ``word`` among compound
        ``parts``. Each part is aligned char-by-char against ``word`` (parts
        preserve the source characters and case); a part character that does not
        match the next source character - e.g. an appended soft hyphen - is
        treated as a zero-width insertion and does not advance the source
        position. The returned spans contiguously cover ``[ns, ne)``; the final
        part absorbs any unaligned remainder so coverage is preserved."""
        spans: List[Tuple[str, int, int]] = []
        i = 0
        last = len(parts) - 1
        for k, part in enumerate(parts):
            start = ns + i
            if k == last:
                spans.append((part, start, ne))
            else:
                for ch in part:
                    if i < len(word) and ch == word[i]:
                        i += 1
                spans.append((part, start, ns + i))
        return spans

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
            return_ranges: Whether to return the ranges (offset, length) of each input word in the joined unescaped text.
            
        Returns:
            The unescaped and joined text.
        """
        words = iter(self.unescape(word, handle_reserved=True) for word in words)
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
            "reserved_tokens": list(self.reserved_tokens_list),
            "preserve_soft_hyphen": self.preserve_soft_hyphen,
            "preserve_format_and_diactritic": self.preserve_format_and_diactritic,
        }

    @staticmethod
    def load_dict(d: dict, **kwargs):
        return PreTokenizer(
            alphabet=kwargs.get("alphabet", d.get("alphabet")),
            normalization=kwargs.get("normalization", d.get("normalization")),
            split_regex=kwargs.get("split_regex", d.get("split_regex")),
            reserved_tokens=kwargs.get("reserved_tokens", d.get("reserved_tokens")),
            preserve_soft_hyphen=kwargs.get("preserve_soft_hyphen", d.get("preserve_soft_hyphen")),
            preserve_format_and_diactritic=kwargs.get("preserve_format_and_diactritic", d.get("preserve_format_and_diactritic", False)),
        )
        