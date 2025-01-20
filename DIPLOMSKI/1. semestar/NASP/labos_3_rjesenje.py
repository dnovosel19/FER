from typing import Tuple


class TrieNode:
    """
    A class to represent a node in a trie
    that contains only the pointers to the used characters
    (as opposed to the whole vocabulary array).

    ...

    Attributes
    ----------

    children : dict[str, TrieNode]
        pointers to the children nodes (for successive characters)
    """

    def __init__(self) -> None:
        self.children = {}


class Trie:

    def __init__(self, terminal: str = '$'):
        self.root = TrieNode()
        self.terminal = terminal

    def insert(self, word: str) -> None:
        """Inserts a word into the trie.

        Args:
            word (str): word to insert
        """
        if self.terminal in word:
            raise Exception(
                f'Explicit terminal ({self.terminal}) use is not allowed within words!')

        node = self.root
        for char in word:
            # TODO: implement the remainder of insertion
            if char not in node.children:
                node.children[char] = TrieNode()
            node =  node.children[char]

        pointer_dict = {}  # TODO: fill in with the right object
        node.children[self.terminal] = None
        # proper terminating the word
        if self.terminal not in pointer_dict:
            pointer_dict[self.terminal] = None

    def search_prefix(self, prefix: str) -> Tuple[bool, TrieNode]:
        """Searches for given prefix in the trie

        Args:
            prefix (str): search term

        Returns:
            bool: True, if the prefix exists in trie
            TrieNode: - THE node that contains all suffixes of the prefix in trie,
                           if the prefix is contained
                      - None, if the prefix is not found
        """
        if self.terminal in prefix:
            raise Exception(
                f'Explicit terminal ({self.terminal}) use is not allowed within words!')
        node = self.root
        for char in prefix:
            # TODO: fill in the missing code
            if char not in node.children:
                return False, None
            node = node.children[char]

        return True, node

    def search(self, word: str) -> bool:
        """Returns if the word is in the trie.

        Args:
            word (str): searching term

        Returns:
            bool: True, if the word is in trie
                  False, otherwise
        """
        # TODO: implement the function
        exists, node = self.search_prefix(word)
        if exists and self.terminal in node.children:
            return True
        return False