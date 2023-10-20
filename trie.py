import json
import schedule

from typing import List, Dict, Optional
from collections import defaultdict


class Trie:
    instance = None
    MAX_NUMBER_OF_SUGGESTIONS = 10
    TERM_FREQUENCY_FILE_NAME = "terms_frequency.json"

    def __new__(cls):
        if not cls.instance:
            cls.instance = super(Trie, cls).__new__(cls)

        return cls.instance

    def __init__(self):
        self.root = TrieNode("", 0, [])
        self.terms_frequency = self.get_terms_frequency()
        self.update_trie()

    def get_suggestions(self, term: str) -> List[str]:
        self.update_term_frequency_in_file(term)

        term_node = self.get_term_node(self.root, term)
        if term_node:
            return [term]

        return []

    def update_term_frequency_in_file(self, term: str) -> None:
        self.terms_frequency[term] += 1
        self.save_terms_frequency(self.terms_frequency)

    def schedule_to_update_trie(self):
        schedule.every(10).seconds.do(self.update_trie)

    def update_trie(self):
        print("Start updating trie")
        new_root = self.copy_trie_starting_from(self.root)

        self.update_terms_frequency_on_trie(new_root)
        self.reset_terms_frequencies()

        self.update_terms_suggestions(new_root)

        self.root = new_root
        print("Finish updating trie")

    def update_terms_frequency_on_trie(self, root: 'TrieNode'):
        for term in self.terms_frequency:
            self.update_term_frequency_on_trie(root, term)

    def update_terms_suggestions(self, root: 'TrieNode'):
        pass

    def update_term_frequency_on_trie(self, root: 'TrieNode', term: str):
        cur_node = root
        for char in term:
            if char not in cur_node.children:
                cur_node.children[char] = TrieNode(char, 0, [])

            cur_node = cur_node.children[char]

        cur_node.frequency += self.terms_frequency[term]

    def get_term_node(self, root: 'TrieNode', term: str) -> Optional['TrieNode']:
        cur_node = root
        for char in term:
            if char not in cur_node.children:
                return None

            cur_node = cur_node.children[char]

        return cur_node

    def copy_trie_starting_from(self, node):
        new_node = TrieNode(node.character, node.frequency, [])

        for child in node.children:
            new_node.children[child] = self.copy_trie_starting_from(node.children[child])

        return new_node

    def print_trie(self, cur_node: 'TrieNode'):
        while cur_node:
            print(cur_node.character)
            for child in cur_node.children:
                child_node = cur_node.children[child]
                self.print_trie(child_node)

    def reset_terms_frequencies(self):
        self.terms_frequency = defaultdict(int)
        self.save_terms_frequency(self.terms_frequency)

    def get_terms_frequency(self):
        with open(self.TERM_FREQUENCY_FILE_NAME, "r") as file:
            try:
                terms_frequency = defaultdict(int, json.load(file))
            except ValueError:
                terms_frequency = defaultdict(int)

            return terms_frequency

    def save_terms_frequency(self, new_terms_frequency: Dict[str, int]) -> None:
        with open(self.TERM_FREQUENCY_FILE_NAME, "w") as file:
            json.dump(new_terms_frequency, file)


class TrieNode:
    def __init__(self, character, frequency, top_suggestions):
        self.character = character
        self.frequency = frequency
        self.top_suggestions = top_suggestions
        self.children = dict()
