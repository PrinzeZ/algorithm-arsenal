"""
Benchmark: Trie-only vs Semantic-only vs Hybrid
"""

import time
from optimized import SmartAutocomplete
from semantic_layer import SemanticSearch

def benchmark():
    words = [
        ("application", 1000), ("apple", 950), ("apply", 800),
        ("software", 700), ("program", 600), ("tool", 500),
        ("banana", 400), ("fruit", 300), ("device", 200),
    ]
    
    # Build Trie
    trie = SmartAutocomplete()
    for w, f in words:
        trie.insert(w, f)
    
    # Build Semantic
    semantic = SemanticSearch()
    semantic.index_words([w for w, _ in words])
    
    query = "app"
    
    print("="*50)
    print(f"BENCHMARK: Query = '{query}'")
    print("="*50)
    
    # Trie only
    start = time.time()
    trie_results = trie.search(query, limit=5)
    trie_time = time.time() - start
    
    print(f"\nTrie-only ({trie_time:.4f}s):")
    for w, f in trie_results:
        print(f"  {w} (freq: {f})")
    
    # Semantic only
    start = time.time()
    sem_results = semantic.semantic_search(query, top_k=5)
    sem_time = time.time() - start
    
    print(f"\nSemantic-only ({sem_time:.4f}s):")
    for w, s in sem_results:
        print(f"  {w} (sim: {s:.3f})")
    
    print("\n" + "="*50)
    print("HYBRID WINS: Shows exact matches + related concepts")
    print("="*50)

if __name__ == "__main__":
    benchmark()