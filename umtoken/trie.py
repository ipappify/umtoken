# Path: umtoken/trie.py

from typing import Any, Tuple

from marisa_trie import Trie

class DictTrie():
    def __init__(self, pairs=None, keys=None, values=None):
        assert (keys is not None and values is not None) or pairs is not None
        if pairs is not None:
            self.trie = Trie([k for k, _ in pairs])
            self.list = [None] * len(self.trie)
            for k, v in pairs:
                self.list[self.trie[k]] = v
        else:
            self.trie = Trie(keys)
            self.list = [None] * len(self.trie)
            for k, v in zip(keys, values):
                self.list[self.trie[k]] = v

    def __getitem__(self, key):
        return self.list[self.trie[key]]
    
    def __len__(self):
        return len(self.trie)
    
    def __contains__(self, key):
        return key in self.trie
    
    def get(self, key, default=None):
        idx = self.trie.get(key, None)
        if idx is not None:
            return self.list[idx]
        return default
    
    def prefixes(self, word) -> list[str]:
        return self.trie.prefixes(word)
    
    def prefixes_and_values(self, word) -> list[Tuple[str, Any]]:
        return [(p, self.list[i]) for p, i in self.trie.iter_prefixes_with_ids(word)]
    
    def values(self, word=None) -> list:
        if word is None:
            return self.list
        return [self.list[i] for _, i in self.trie.iter_prefixes_with_ids(word)]

    
class LookupTrie():
    def __init__(self, pairs=None, keys=None, values=None):
        assert (keys is not None and values is not None) or pairs is not None
        if pairs is not None:
            self.trie = Trie([k for k, _ in pairs])
            self.list = [[] for _ in self.trie]
            for k, v in pairs:
                self.list[self.trie[k]].append(v)
        else:
            self.trie = Trie(keys)
            self.list = [[] for _ in self.trie]
            for k, v in zip(keys, values):
                self.list[self.trie[k]].append(v)

    def __getitem__(self, key):
        return self.list[self.trie[key]]
    
    def __len__(self):
        return len(self.trie)
    
    def __contains__(self, key):
        return key in self.trie
    
    def prefixes(self, word) -> list[str]:
        return self.trie.prefixes(word)
    
    def prefixes_and_values(self, word) -> list[Tuple[str, list]]:
        return [(p, self.list[i]) for p, i in self.trie.iter_prefixes_with_ids(word)]
    
    def values(self, word) -> list[list]:
        return [self.list[i] for _, i in self.trie.iter_prefixes_with_ids(word)]

    
