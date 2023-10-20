import schedule

from trie import Trie


if __name__ == '__main__':
    trie = Trie()
    trie.schedule_to_update_trie()

    while True:
        schedule.run_pending()
        term = input("Enter term: ").strip()
        suggestions = trie.get_suggestions(term)
        print(suggestions)
