from typing import Dict

from mlcc.common.defaults import TRIE_END_OF_WORD


class TrieNode:

    def __init__(self, is_word: bool = False):
        self.children: Dict[str, TrieNode] = {}

    def __str__(self) -> str:
        return f"{self.children}"

    def __repr__(self) -> str:
        return str(self)

    def add_word(self, word: str) -> None:
        if len(word) == 0:
            self.children.setdefault(TRIE_END_OF_WORD, TrieNode())
        else:
            self.children.setdefault(word[0], TrieNode()).add_word(word[1:])

    def get_longest_unique_prefix(self) -> str:
        if len(self.children) == 1 and TRIE_END_OF_WORD not in self.children:
            return list(self.children.keys())[0] + list(self.children.values())[0].get_longest_unique_prefix()
        return ""

    def get_next_chars(self, prefix: str = "") -> Dict[str, str]:
        result: Dict[str, str] = {}
        for k, v in self.children.items():
            if k != TRIE_END_OF_WORD:
                result[k] = k + v.get_longest_unique_prefix()
        return result

    def is_word(self, word: str) -> bool:
        if len(word) == 0:
            return TRIE_END_OF_WORD in self.children
        if word[0] in self.children:
            return self.children[word[0]].is_word(word[1:])
        return False
