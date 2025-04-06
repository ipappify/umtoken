# Path: umtoken/vocab.py

import json
from collections import Counter
from typing import Optional, Iterable

from tqdm import tqdm

from .pre import PreTokenizer

def extract_vocab(text_iterator: Iterable[str], 
                  normalization: Optional[str] = "default",
                  min_frequency: Optional[int] = None,
                  progress=True,
                  check=True) -> Counter:
    """
    Extracts the vocabulary from a text iterator.
    
    Args:
        text_iterator: An iterator of text.
        normalization: The normalization to use. See PreTokenizer for more information.
        min_frequency: The minimum frequency of a word to be included in the vocabulary.
        
    Returns:
        A Counter of the vocabulary.
    """
    pre = PreTokenizer(normalization=normalization)
    vocab = Counter()
    if progress:
        text_iterator = tqdm(text_iterator, desc="Extracting vocabulary...")
    
    for text in text_iterator:
        if check and text.startswith("bytearray(b'"):
            raise ValueError("The text iterator contains byte strings. Please decode them to str.")
        
        words = pre.split(text)
        for word in words:
            # same order as in PreTokenizer: split, normalize, strip blank, lower
            word = pre.normalize(word)
            if not word:
                continue            
            word = word.strip(" ") if len(word) > 1 else word
            word = word.lower()
            vocab[word] += 1
    if min_frequency:
        vocab = Counter({word: count for word, count in vocab.items() if count >= min_frequency})
    return vocab

def save_vocab(vocab: Counter, path: str, unordered: bool = False):
    """
    Saves a vocabulary to a json or jsonl file.
    
    Args:
        vocab: The vocabulary to save.
        path: The path to save the vocabulary to.
    """
    with open(path, "w", encoding="utf8") as f:
        if not unordered:
            if not isinstance(vocab, Counter):
                vocab = Counter(vocab)
            vocab = {w: c for w, c in vocab.most_common()}
        if path.endswith(".json"):
            json.dump(vocab, f, ensure_ascii=False, indent=0)
        elif path.endswith(".jsonl"):
            for word, count in vocab.items():
                f.write(f"{json.dumps([word,count], ensure_ascii=False)}\n")
        else:
            raise ValueError(f"Unsupported file format: {path}")
            
def load_vocab(path: str) -> Counter:
    """
    Loads a vocabulary from a json or jsonl file.
    
    Args:
        path: The path to load the vocabulary from.
        
    Returns:
        The vocabulary.
    """
    with open(path, "r", encoding="utf8") as f:
        if path.endswith(".json"):
            return Counter(json.load(f))
        else:
            vocab = Counter()
            for line in f:
                word, count = json.loads(line)
                vocab[word] = count
        