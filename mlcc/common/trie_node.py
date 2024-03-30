from typing import Dict


class TrieNode:

    def __init__(self, is_word: bool = False):
        self.children: Dict[str, TrieNode] = {}
        self.is_word = is_word

    def __str__(self) -> str:
        return f"{self.children}"

    def __repr__(self) -> str:
        return str(self)

    def add_word(self, word: str) -> None:
        if len(word) == 0:
            self.is_word = True
        else:
            self.children.setdefault(word[0], TrieNode()).add_word(word[1:])

    def get_longest_unique_prefix(self) -> str:
        if len(self.children) == 1:
            return list(self.children.keys())[0] + list(self.children.values())[0].get_longest_unique_prefix()
        return ""

    def get_next_chars(self) -> Dict[str, str]:
        result: Dict[str, str] = {}
        for k, v in self.children.items():
            result[k] = k + v.get_longest_unique_prefix()
        return result
