"""
HYBRID SEARCH: Trie (lexical) + Semantic (meaning)
Uses optimized Trie with min-heap pre-computation
"""

from optimized import SmartAutocomplete
from semantic_layer import SemanticSearch


class HybridAutocomplete:
    def __init__(self):
        self.trie = SmartAutocomplete(k=10)  # Store top 10 for flexibility
        self.semantic = SemanticSearch()
        self.max_freq = 1
        self._index_built = False
    
    def build_index(self, words_with_freq):
        """Build both indexes"""
        self.max_freq = max(freq for _, freq in words_with_freq)
        
        for word, freq in words_with_freq:
            self.trie.insert(word, freq)
        
        word_list = [w for w, _ in words_with_freq]
        self.semantic.index_words(word_list)
        self._index_built = True
        print("Hybrid index built!")
    
    def hybrid_search(self, query, limit=5):
        """Combine Trie + Semantic scores"""
        if not self._index_built:
            return []
        
        # Trie: instant prefix matches
        trie_results = self.trie.search(query, limit=limit)
        
        # Semantic: meaning matches
        semantic_results = self.semantic.semantic_search(query, top_k=limit * 2)
        
        # Merge scores
        candidates = {}
        
        # Trie scores (normalized 0-1)
        for freq, word in trie_results:  # Note: (freq, word) from new Trie
            trie_score = freq / self.max_freq
            candidates[word] = {
                'trie_score': trie_score,
                'semantic_score': 0.0,
                'source': 'trie'
            }
        
        # Semantic scores
        for word, sim_score in semantic_results:
            if word in candidates:
                candidates[word]['semantic_score'] = sim_score
                candidates[word]['source'] = 'both'
            else:
                candidates[word] = {
                    'trie_score': 0.0,
                    'semantic_score': sim_score,
                    'source': 'semantic'
                }
        
        # Final hybrid score
        final = []
        for word, scores in candidates.items():
            hybrid = (0.6 * scores['trie_score']) + (0.4 * scores['semantic_score'])
            final.append({
                'word': word,
                'score': hybrid,
                'trie': scores['trie_score'],
                'semantic': scores['semantic_score'],
                'source': scores['source']
            })
        
        final.sort(key=lambda x: x['score'], reverse=True)
        return final[:limit]


# --- TEST ---
if __name__ == "__main__":
    hybrid = HybridAutocomplete()
    
    words = [
        ("application", 1000), ("apple", 950), ("apply", 800),
        ("software", 700), ("program", 600), ("tool", 500),
        ("banana", 400), ("fruit", 300), ("device", 200),
    ]
    
    hybrid.build_index(words)
    
    print("\n" + "="*50)
    print("HYBRID SEARCH: 'app'")
    print("="*50)
    
    for r in hybrid.hybrid_search("app", limit=6):
        print(f"\n  {r['word']}")
        print(f"    Score: {r['score']:.3f} (Trie: {r['trie']:.3f}, Semantic: {r['semantic']:.3f})")
        print(f"    Source: {r['source']}")