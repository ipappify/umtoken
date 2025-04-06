from enum import Enum
import os
from typing import Dict, List, Optional, Tuple, Union

from transformers import PreTrainedTokenizerBase, TensorType, BatchEncoding
from transformers.tokenization_utils_base import (PaddingStrategy, TruncationStrategy, 
                                                  TextInput, PreTokenizedInput, EncodedInput,
                                                  TextInputPair, PreTokenizedInputPair, EncodedInputPair)

from ..tokenizer import Tokenizer
from ..pre import PAD_TOKEN

class PropIdHandling(Enum):
    PACK = 0
    TOKEN_TYPE_ID = 1
    DISCARD = 2

class UnimorphTokenizer(PreTrainedTokenizerBase):
    def __init__(self, 
                 tokenizer: Tokenizer, 
                 prop_id_handling: PropIdHandling = PropIdHandling.PACK,
                 pack_stride: Optional[int] = None, 
                 force_slow: bool = False, 
                 pad_token: str = PAD_TOKEN,
                 prefix: Optional[str] = None,
                 suffix: Optional[str] = None,
                 **kwargs):
        """
        A wrapper for a Tokenizer that provides the same interface as a "slow" Hugging Face tokenizer.
        
        Args:
            tokenizer: The Tokenizer to wrap.
            prop_id_handling: How to handle prop ids. One of PropIdHandling.PACK, PropIdHandling.TOKEN_TYPE_ID, PropIdHandling.DISCARD.
            pack_stride: The stride for packing prop ids. If None, the stride is the vocabulary size.
            force_slow: Whether to force slow tokenization. This prevents building a stem trie and is useful when only a few words need to be encoded.
            pad_token: The pad token.
            prefix: The prefix to prepend to the tokenized text.
            suffix: The suffix to append to the tokenized text.
            kwargs: Additional arguments.
        """
        
        super().__init__(**kwargs)

        assert prop_id_handling in PropIdHandling, "prop_id_handling must be a PropIdHandling enum"
        
        if prop_id_handling == PropIdHandling.PACK and pack_stride is not None:
            assert len(tokenizer.model.vocab) <= pack_stride, "Vocabulary too large for packing with pack_stride"

        self.tokenizer = tokenizer
        self.prop_id_handling = prop_id_handling
        self.pack_stride = pack_stride
        self.force_slow = force_slow
        self.pad_token = pad_token
        self.prefix = prefix
        self.suffix = suffix
        
        self.prefix_ids = None
        self.suffix_ids = None

    @staticmethod
    def from_pretrained(pretrained_model_name_or_path: Union[str, os.PathLike, Tokenizer],
                        cache_dir: Optional[Union[str, os.PathLike]] = None,
                        force_download: bool = False,
                        local_files_only: bool = False,
                        token: Optional[Union[str, bool]] = None,
                        revision: str = "main",
                        trust_remote_code=False,
                        prop_id_handling: PropIdHandling = PropIdHandling.PACK,
                        pack_stride: Optional[int] = None, 
                        force_slow: bool = False, 
                        **kwargs,):
        name_or_path = pretrained_model_name_or_path

        kwargs["prop_id_handling"] = prop_id_handling
        kwargs["pack_stride"] = pack_stride
        kwargs["force_slow"] = force_slow

        if isinstance(name_or_path, Tokenizer):
            kwargs["name_or_path"] = "umtoken"
            tokenizer = name_or_path
            return UnimorphTokenizer(tokenizer, **kwargs)
        elif (isinstance(name_or_path, os.PathLike) or  
              (isinstance(name_or_path, str) and os.path.isfile(name_or_path))):
            kwargs["name_or_path"] = name_or_path
            tokenizer = Tokenizer.load(name_or_path)
            return UnimorphTokenizer(tokenizer, **kwargs)
        else:
            raise NotImplementedError("Loading from hf is not supported yet")
        
    def __len__(self) -> int:
        stride = self.pack_stride or self.len_vocab()
        return stride * self.len_props() if self.prop_id_handling == PropIdHandling.PACK else self.len_vocab()

    def get_vocab(self) -> Dict[str, int]:
        return {v: i for i, v in enumerate(self.tokenizer.model.vocab)}
    
    def len_vocab(self) -> int:
        return len(self.tokenizer.model.vocab) 

    def len_props(self) -> int:
        return 6 * len(self.tokenizer.model.rules)
    
    def save_pretrained(
        self,
        save_directory: Union[str, os.PathLike],
        legacy_format: Optional[bool] = None,
        filename_prefix: Optional[str] = None,
        push_to_hub: bool = False,
        **kwargs,
    ) -> Tuple[str]:
        raise NotImplementedError("Saving is not supported yet. Save the inner tokenizer instead.")
    
    def save_vocabulary(self, save_directory: str, filename_prefix: Optional[str] = None) -> Tuple[str]:
        raise NotImplementedError("Saving vocabulary is not supported yet.")

    def tokenize(self, text: str, pair: Optional[str] = None, add_special_tokens: bool = False, **kwargs) -> List[str]:
        # TODO: should we decompose and format the tokens?
        raise NotImplementedError
    
    def num_special_tokens_to_add(self, pair: bool = False) -> int:
        raise NotImplementedError
    
    def convert_tokens_to_ids(self, tokens: Union[str, List[str]]) -> Union[int, List[int]]:
        # TODO: should we decompose the tokens? Or should we expect them to be decomposed and formatted?
        if isinstance(tokens, str):
            return self.tokenizer.model.vocab_lookup[tokens]
        return [self.tokenizer.model.vocab_lookup[t] for t in tokens]
    
    def set_prefix(self, prefix: Optional[str] = None):
        self.prefix = prefix
        self.prefix_ids = None
        
    def set_suffix(self, suffix: Optional[str] = None):
        self.suffix = suffix
        self.suffix_ids = None
    
    def _encode_plus(
        self,
        text: Union[TextInput, PreTokenizedInput, EncodedInput],
        text_pair: Optional[Union[TextInput, PreTokenizedInput, EncodedInput]] = None,
        add_special_tokens: bool = True,
        padding_strategy: PaddingStrategy = PaddingStrategy.DO_NOT_PAD,
        truncation_strategy: TruncationStrategy = TruncationStrategy.DO_NOT_TRUNCATE,
        max_length: Optional[int] = None,
        stride: int = 0,
        is_split_into_words: bool = False,
        pad_to_multiple_of: Optional[int] = None,
        padding_side: Optional[bool] = None,
        return_tensors: Optional[Union[str, TensorType]] = None,
        return_token_type_ids: Optional[bool] = None,
        return_attention_mask: Optional[bool] = None,
        return_overflowing_tokens: bool = False,
        return_special_tokens_mask: bool = False,
        return_offsets_mapping: bool = False,
        return_length: bool = False,
        verbose: bool = True,
        split_special_tokens: bool = False,
        **kwargs,
    ) -> BatchEncoding:
        assert text_pair is None, "text_pair is not supported yet"

        if is_split_into_words:
            assert isinstance(text, list) and all(isinstance(t, str) for t in text), "text must be a list of strings if is_split_into_words is True"
        else:
            assert isinstance(text, str), "text must be a string if is_split_into_words is False"

        # encode as batch
        enc = self._batch_encode_plus(
            [text],
            add_special_tokens=add_special_tokens,
            padding_strategy=padding_strategy,
            truncation_strategy=truncation_strategy,
            max_length=max_length,
            stride=stride,
            is_split_into_words=is_split_into_words,
            pad_to_multiple_of=pad_to_multiple_of,
            padding_side=padding_side,
            return_tensors=return_tensors,
            return_token_type_ids=return_token_type_ids,
            return_attention_mask=return_attention_mask,
            return_overflowing_tokens=return_overflowing_tokens,
            return_special_tokens_mask=return_special_tokens_mask,
            return_offsets_mapping=return_offsets_mapping,
            return_length=return_length,
            verbose=verbose,
            split_special_tokens=split_special_tokens,
            **kwargs,
        )

        # remove batch dimension
        return BatchEncoding({k: v[0] for k, v in enc.items()})

    def _batch_encode_plus(
        self,
        batch_text_or_text_pairs: Union[
            List[TextInput],
            List[TextInputPair],
            List[PreTokenizedInput],
            List[PreTokenizedInputPair],
            List[EncodedInput],
            List[EncodedInputPair],
        ],
        add_special_tokens: bool = True,
        padding_strategy: PaddingStrategy = PaddingStrategy.DO_NOT_PAD,
        truncation_strategy: TruncationStrategy = TruncationStrategy.DO_NOT_TRUNCATE,
        max_length: Optional[int] = None,
        stride: int = 0,
        is_split_into_words: bool = False,
        pad_to_multiple_of: Optional[int] = None,
        padding_side: Optional[bool] = None,
        return_tensors: Optional[Union[str, TensorType]] = None,
        return_token_type_ids: Optional[bool] = None,
        return_attention_mask: Optional[bool] = None,
        return_overflowing_tokens: bool = False,
        return_special_tokens_mask: bool = False,
        return_offsets_mapping: bool = False,
        return_length: bool = False,
        verbose: bool = True,
        split_special_tokens: bool = False,
        **kwargs,
    ) -> BatchEncoding:
        assert stride == 0, "stride is not supported yet (what is stride?)"
        assert return_token_type_ids is None, "return_token_type_ids is not supported yet"
        assert return_overflowing_tokens == False, "return_overflowing_tokens is not supported yet"
        assert return_special_tokens_mask == False, "return_special_tokens_mask is not supported yet"
        assert return_offsets_mapping == False, "return_offsets_mapping is not supported yet"
        assert return_length == False, "return_length is not supported yet"
        
        assert truncation_strategy == TruncationStrategy.DO_NOT_TRUNCATE or max_length, "max_length must be provided if truncation_strategy is not DO_NOT_TRUNCATE"

        # TODO: not sure how to return pairs
        assert isinstance(batch_text_or_text_pairs, list), "batch_text_or_text_pairs must be a list"
        for text in batch_text_or_text_pairs:
            if is_split_into_words:
                assert isinstance(text, list) and all(isinstance(t, str) for t in text), "each text must be a list of strings if is_split_into_words is True (pairs are not supported yet)"
            else:
                assert isinstance(text, str), "each text must be a string if is_split_into_words is False (pairs are not supported yet)"

        local_cache = {}
        encs = []
        for text in batch_text_or_text_pairs:
            # tokenize
            ids = self.tokenizer.tokenize(text, 
                                          is_split_and_escaped=is_split_into_words,
                                          handle_reserved=not split_special_tokens, 
                                          return_ranges=False,
                                          local_cache=local_cache, 
                                          force_slow=self.force_slow)
            
            if add_special_tokens and self.prefix:
                if self.prefix_ids is None:
                    self.prefix_ids = self.tokenizer.tokenize(self.prefix, 
                                                              is_split_and_escaped=False,
                                                              handle_reserved=True, 
                                                              return_ranges=False,
                                                              force_slow=self.force_slow)
                ids = self.prefix_ids + ids

            if add_special_tokens and self.suffix:
                if self.suffix_ids is None:
                    self.suffix_ids = self.tokenizer.tokenize(self.suffix, 
                                                              is_split_and_escaped=False,
                                                              handle_reserved=True, 
                                                              return_ranges=False,
                                                              force_slow=self.force_slow)
                ids = ids + self.suffix_ids

            # truncate
            if truncation_strategy != TruncationStrategy.DO_NOT_TRUNCATE and len(ids) > max_length:
                ids = ids[:max_length]

            # TODO: not entirely sure about BatchEncoding - which data is actually handled by super().pad(...)?
            if self.prop_id_handling == PropIdHandling.PACK:
                # pack ids
                stride = self.pack_stride or self.len_vocab()
                packed_ids = [v_id + stride * p_id for v_id, p_id in ids]
                enc = BatchEncoding(data={
                    "input_ids": packed_ids,
                    "token_type_ids": [0] * len(packed_ids),
                    "attention_mask": [1] * len(packed_ids),
                })
            elif self.prop_id_handling == PropIdHandling.TOKEN_TYPE_ID:
                # separate ids
                enc = BatchEncoding(data={
                    "input_ids": [v_id for v_id, _ in ids],
                    "token_type_ids": [p_id for _, p_id in ids],
                    "attention_mask": [1] * len(ids),
                })
            elif self.prop_id_handling == PropIdHandling.DISCARD:
                # discard prop ids
                enc = BatchEncoding(data={
                    "input_ids": [v_id for v_id, _ in ids],
                    "token_type_ids": [0] * len(ids),
                    "attention_mask": [1] * len(ids),
                })
            else:
                raise ValueError(f"Unknown prop_id_handling: {self.prop_id_handling}")
            encs.append(enc)

        return self.pad(encs, padding_strategy, max_length, 
                        pad_to_multiple_of, padding_side, 
                        return_attention_mask, return_tensors, verbose)
    
    def _decode(
        self,
        token_ids: Union[int, List[int]],
        skip_special_tokens: bool = False,
        clean_up_tokenization_spaces: bool = None,
        prop_ids: Optional[Union[int, List[int]]] = None,
        prop_id_handling: Optional[PropIdHandling] = None,
        **kwargs,
    ) -> str:
        if isinstance(token_ids, int):
            token_ids = [token_ids]
        if isinstance(prop_ids, int):
            prop_ids = [prop_ids]
        prop_id_handling = prop_id_handling if prop_id_handling is not None else self.prop_id_handling
        if prop_id_handling == PropIdHandling.PACK:
            stride = self.pack_stride or self.len_vocab()
            ids = [(t_id % stride, t_id // stride) for t_id in token_ids]
        elif prop_id_handling == PropIdHandling.TOKEN_TYPE_ID:
            assert prop_ids is not None, "prop_ids must be provided if prop_id_handling is TOKEN_TYPE_ID"
            ids = [(t_id, p_id) for t_id, p_id in zip(token_ids, prop_ids)]
        elif prop_id_handling == PropIdHandling.DISCARD:
            ids = [(t_id, 0) for t_id in token_ids]
        else:
            raise ValueError(f"Unknown prop_id_handling: {prop_id_handling}")
        
        return self.tokenizer.detokenize(ids, omit_reserved=skip_special_tokens, **kwargs)
