"""
HYBRID SEARCH: Trie (lexical) + Semantic (meaning)
Merges prefix matching with vector similarity for intelligent autocomplete
"""
import os
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

from optimized import SmartAutocomplete
from semantic_layer import SemanticSearch


class HybridAutocomplete:
    def __init__(self):
        self.trie = SmartAutocomplete()
        self.semantic = SemanticSearch()
        self.max_freq = 1
        self._index_built = False
    
    def build_index(self, words_with_freq):
        """Build both Trie and Semantic indexes"""
        self.max_freq = max(freq for _, freq in words_with_freq)
        
        for word, freq in words_with_freq:
            self.trie.insert(word, freq)
        
        word_list = [word for word, _ in words_with_freq]
        self.semantic.index_words(word_list)
        self._index_built = True
        
        print("Hybrid index built!")
    
    def hybrid_search(self, query, limit=5):
        """Combine Trie + Semantic scores"""
        if not self._index_built:
            print("ERROR: Call build_index() first!")
            return []
        
        # Trie results: prefix matches
        trie_results = self.trie.search(query, limit=limit)
        
        # Semantic results: meaning matches
        semantic_results = self.semantic.semantic_search(query, top_k=limit * 2)
        
        # Build candidate scores
        candidates = {}
        
        # Trie scores (normalized)
        for word, freq in trie_results:
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
        
        # Calculate final scores
        final = []
        for word, scores in candidates.items():
            hybrid_score = (0.6 * scores['trie_score']) + (0.4 * scores['semantic_score'])
            final.append({
                'word': word,
                'score': hybrid_score,
                'trie': scores['trie_score'],
                'semantic': scores['semantic_score'],
                'source': scores['source']
            })
        
        # Sort by hybrid score
        final.sort(key=lambda x: x['score'], reverse=True)
        return final[:limit]


# --- TEST ---
if __name__ == "__main__":
    hybrid = HybridAutocomplete()
    
    words = [
        ("application", 1000),
        ("apple", 950),
        ("apply", 800),
        ("software", 700),
        ("program", 600),
        ("tool", 500),
        ("banana", 400),
        ("fruit", 300),
    ]
    
    hybrid.build_index(words)
    
    print("\n" + "="*50)
    print("HYBRID SEARCH: 'app'")
    print("="*50)
    
    results = hybrid.hybrid_search("app", limit=6)
    
    for r in results:
        print(f"\n  {r['word']}")
        print(f"    Score: {r['score']:.3f} (Trie: {r['trie']:.3f}, Semantic: {r['semantic']:.3f})")
        print(f"    Source: {r['source']}")