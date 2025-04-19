# Path: umtoken/tokenizer.py

import json
from typing import List, Optional, Tuple, Union
from warnings import warn

from .alphabet import ASCII_ENCODING_SPACE as SP, ASCII_RESERVED_UPPER as UP
from .pre import PreTokenizer
from .model import Model
from .utils import cumsum

class Tokenizer():
    def __init__(self, 
                 pre: PreTokenizer,
                 model: Model,
                 thumbprint: Optional[str] = None):
        """
        A tokenizer.
        
        Args:
            pre: The pre-tokenizer.
            model: The tokenizer model.
            thumbprint: A thumbprint for identifying the tokenizer.
        """
        self.pre = pre
        self.model = model
        self.thumbprint = thumbprint
        self.reserves_token_ids = frozenset(model.vocab_lookup[t] for t in pre.reserved_tokens)
        
    def tokenize(self, 
                 text: str, 
                 handle_reserved: bool = False, 
                 allowed_reserved: Optional[list[str]] = None,
                 is_split_and_escaped: bool = False,
                 merge_prop_ids: bool = True,
                 return_ranges: bool = False,
                 force_slow: bool = False,
                 local_cache: Optional[dict] = None):
        """
        Tokenizes text into tuples of token ids.
        
        Args:
            text: The text to tokenize.
            handle_reserved: Whether to handle reserved tokens.
            allowed_reserved: A list of reserved tokens to allow. If not set, all reserved tokens are allowed.
            is_split_and_escaped: Whether the text is already split and escaped (string of escaped words separated by blanks).
            merge_prop_ids: Property ids (rule_id, case_id, space_id) are merged into a single id: rule_id * 6 + case_id * 2 + space_id
            return_ranges: Whether to return the ranges of the words (offset, length).
            force_slow: Whether to force slow decomposition. This avoids building a stem trie and is useful when only a few words need to be encoded.
            local_cache: A local cache for storing token ids.

        Returns:
            If return_ranges is False, the list of token ids (tuples). Tuples are either: (vocab_id, aux_id) or (vocab_id, rule_id, case_id, space_id)
            If return_ranges is True, a tuple of the list of token ids, the list of word ranges, and a mapping of tokens to words.
        """
        if is_split_and_escaped:
            assert return_ranges == False, "Ranges are not supported for split and escaped text."
            is_tuple = False
            words = text.split(" ") if isinstance(text, str) else text
        else:
            is_tuple = True
            words, word_ranges = self.pre.split_and_escape(text, 
                                                           handle_reserved=handle_reserved,
                                                           allowed_reserved=allowed_reserved,
                                                           return_ranges=True,
                                                           return_as_tuple=True)
        tokens = []
        tokens_to_words = []
        local_cache = local_cache or {}
        for i, word in enumerate(words):
            try:
                if not is_tuple:
                    # strip UP and SP from word
                    ws_id = 0 # 0: no space, 1: one space - other cases are handles by pre tokenizer
                    up_id = 0 # 0: lower case, 1: title case, 2: all upper case
                    if len(word) > 1:
                        ws_id = 1 if word[0] == SP and word[1] != SP else 0
                        if ws_id:
                            word = word[ws_id:]
                        up_id = 1 if word[0] == UP else 0
                        up_id += 1 if word[1] == UP else 0
                        if up_id:
                            word = word[up_id:]
                else:
                    word, ws_id, up_id = word
                        
                # apply model
                ids = local_cache.get(word, None)
                if ids is None:
                    if handle_reserved and word in self.pre.reserved_tokens:
                        if allowed_reserved is None or word in allowed_reserved:
                            ids = [(self.model.vocab_lookup[word], 0)]
                        else:
                            ids = self.model.encode(word, force_slow=force_slow)
                    else:
                        ids = self.model.encode(word, force_slow=force_slow)
                    local_cache[word] = ids
                # combine ids
                if merge_prop_ids:
                    ids = [(v_id, r_id * 6 + (up_id * 2 + ws_id if i == 0 else 0)) for i, (v_id, r_id) in enumerate(ids)]
                else:
                    ids = [(v_id, r_id, up_id if i == 0 else 0, ws_id if i == 0 else 0) for i, (v_id, r_id) in enumerate(ids)]
                # append tokens and word index
                tokens.extend(ids)
                tokens_to_words.extend([i] * len(ids))
            except Exception as e:
                warn(f"Error tokenizing word '{word}': {e}")
                tokens.append((self.model.unk_token_id, 0))
                tokens_to_words.append(i)
        return (tokens, word_ranges, tokens_to_words) if return_ranges else tokens
    
    def detokenize(self, 
                   ids: List[Union[Tuple[int, int], Tuple[int, int, int, int]]], 
                   omit_reserved: bool = True, 
                   return_ranges: bool = False) -> Union[str, Tuple[str, List[Tuple[int, int]], List[int]]]:
        """
        Detokenizes a list of token ids into text.
        
        Args:
            ids: The list of token ids.
            omit_reserved: Whether to omit reserved tokens.
            return_ranges: Whether to return the ranges of the words (offset, length).
            
        Returns:
            If return_ranges is False, the detokenized text.
            If return_ranges is True, a tuple of the detokenized text, the list of word ranges, and a mapping of tokens to words.
        """
        if len(ids) == 0:
            return ("", [], []) if return_ranges else ""
        merged_prop_ids = len(ids[0]) == 2
        words = []
        tokens_to_words = []
        cur_tokens = []
        cur_up = 0
        cur_ws = 0
        cur_new = True
        for i, t_id in enumerate(ids):
            if merged_prop_ids:
                v_id = t_id[0]
                a_id = t_id[1]
                r_id = a_id // 6
                up_id = a_id % 6 // 2
                ws_id = a_id % 2
            else:
                v_id, r_id, up_id, ws_id = t_id

            if cur_new:
                cur_ws = ws_id
                cur_up = up_id
                cur_new = False

            # reserved tokens are always EOW rules
            res = v_id in self.reserves_token_ids
            eow = self.model.is_eow_rule[r_id] or res
            cur_tokens.append((v_id, r_id))
            tokens_to_words.append(len(words))

            if eow:
                if res:
                    # words should not be merged with reserved tokens, 
                    # but model output may not be perfect and needs to handled properly.
                    # if the last token is a reserved token, it should be treated as a separate word
                    if len(cur_tokens) > 1:
                        # emit the real word
                        word = self.model.decode(cur_tokens[:-1])
                        word = self.pre.unescape((word, cur_ws, cur_up))
                        words.append(word)
                        # set reserved token to be the next word
                        cur_tokens = cur_tokens[-1:]
                        tokens_to_words[-1] = len(words)
                    if omit_reserved:
                        words.append("")
                    else:
                        # no need to unescape reserved tokens
                        words.append(self.model.decode(cur_tokens))
                else:
                    word = self.model.decode(cur_tokens)
                    word = self.pre.unescape((word, cur_ws, cur_up))
                    words.append(word)
                cur_tokens = []
                cur_new = True

        if len(cur_tokens) > 0:
            word = self.model.decode(cur_tokens)
            if omit_reserved and word in self.pre.reserved_tokens:
                words.append("")
            else:
                word = SP * cur_ws + UP * cur_up + word
                word = self.pre.unescape(word)
                words.append(word)

        text = "".join(words)
        if not return_ranges:
            return text
        else:
            word_offsets = cumsum(len(w) for w in words)
            word_ranges = [(offset, len(word)) for word, offset in zip(words, word_offsets)]
            return text, word_ranges, tokens_to_words
    
    def save_dict(self) -> dict:
        return {
            "pre": self.pre.save_dict(),
            "model": self.model.save_dict(),
            "thumbprint": self.thumbprint
        }
    
    @staticmethod
    def load_dict(d: dict):
        pre = PreTokenizer.load_dict(d["pre"])
        model = Model.load_dict(d["model"])
        thumbprint = d.get("thumbprint")
        return Tokenizer(pre, model, thumbprint)
    
    def save(self, path: str):
        """
        Saves the tokenizer to a json file.
        
        Args:
            path: The path to the json file.
        """
        d = self.save_dict()
        with open(path, 'w', encoding="utf8") as f:
            json.dump(d, f, ensure_ascii=False, indent=None)

    @staticmethod
    def load(path: str):
        """
        Loads a tokenizer from a json file.
        
        Args:
            path: The path to the json file.

        Returns:
            The loaded tokenizer.
        """
        with open(path, 'r', encoding="utf8") as f:
            d = json.load(f)
        return Tokenizer.load_dict(d)