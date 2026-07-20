import heapq

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.top_k = []  # Only store top K words at this node

class SmartAutocomplete:
    def __init__(self, k=5):
        self.root = TrieNode()
        self.k = k
    
    def insert(self, word, frequency=1):
        node = self.root
        
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            
            # Maintain top K at this node using a min-heap
            # Store (-frequency, word) for max-heap behavior
            if len(node.top_k) < self.k:
                heapq.heappush(node.top_k, (frequency, word))
            elif frequency > node.top_k[0][0]:
                heapq.heapreplace(node.top_k, (frequency, word))
        
        node.is_end_of_word = True
    
    def search(self, prefix, limit=5):
        node = self.root
        
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        
        # Return sorted results (highest frequency first)
        # top_k is a min-heap, so sort in reverse
        results = sorted(node.top_k, key=lambda x: x[0], reverse=True)
        return results[:limit]