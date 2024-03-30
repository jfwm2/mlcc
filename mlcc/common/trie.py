from typing import Dict

from mlcc.common.trie_node import TrieNode


class Trie:

    def __init__(self) -> None:
        self.root = TrieNode()

    def __str__(self) -> str:
        return str(self.root)

    def __repr__(self) -> str:
        return str(self)

    def add_word(self, word: str) -> None:
        self.root.add_word(word)

    def is_word(self, word: str) -> bool:
        return self.root.is_word(word)

    def get_next_chars(self, prefix: str = "") -> Dict[str, str]:
        current_node = self.root
        for char in prefix:
            current_node = current_node.children.get(char)
        return current_node.get_next_chars()
