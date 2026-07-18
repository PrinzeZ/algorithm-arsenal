class TrieNode:
    def __init__(self):
        self.children = {}  #a way to say "from this letter, where can 
                                #I go next?" (like a map/dictionary)
        
        self.is_end_of_word = False
        self.words_below =[]
        
class SmartAutocomplete:
    def __init__(self):
        """Add a word to the tree"""
        self.root = TrieNode()
        
    def insert(self, word, frequency=1):
        """
        frequency = how popular this word is (higher = more popular)
        """
        node = self.root
    
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            
            node = node.children[char]
            node.words_below.append((word, frequency))  # store tuple now
        
        node.is_end_of_word = True
    def search(self, prefix, limit=5):
        """Find all words starting with prefix"""
        node = self.root
        
        # Walk down the tree following the prefix
        for char in prefix:
            if char not in node.children:
                return []  # No matches at all
            node = node.children[char]
        
        # NOW sort - only once, after we reach the final node!
        results = sorted(node.words_below, key=lambda x: x[1], reverse=True)
        
        # Remove duplicates and return just the words
        seen = set()
        unique_results = []
        for word, freq in results:
            if word not in seen:
                seen.add(word)
                unique_results.append((word, freq))
                if len(unique_results) >= limit:
                    break
        
        return unique_results
    
# --- TEST WITH RANKING ---
ac = SmartAutocomplete()

# Insert with popularity scores
ac.insert("application", 1000)   # Very popular
ac.insert("apple", 950)          # Popular
ac.insert("apply", 800)          # Kinda popular
ac.insert("appetizer", 100)      # Not popular
ac.insert("banana", 500)
ac.insert("bandana", 200)

print("Top results for 'app':")
for word, freq in ac.search("app",limit=4):
    print(f"  {word} (popularity: {freq})")