class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.topic_data = None  # Store topic details when a word ends

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, title, topic_data):
        node = self.root
        for char in title.lower():
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.topic_data = topic_data

    def search(self, prefix):
        """
        Returns a list of topics that match the prefix.
        """
        node = self.root
        for char in prefix.lower():
            if char not in node.children:
                return []
            node = node.children[char]

        return self._collect_all_words(node)

    def _collect_all_words(self, node, results=None):
        if results is None:
            results = []
        if node.is_end_of_word:
            results.append(node.topic_data)
        for child in node.children.values():
            self._collect_all_words(child, results)
        return results
