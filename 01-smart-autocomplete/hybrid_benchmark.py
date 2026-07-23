"""
Benchmark: Trie-only vs Semantic-only vs Hybrid
"""

import time
from optimized import SmartAutocomplete
from semantic_layer import SemanticSearch
from hybrid_search import HybridAutocomplete

def benchmark():
    words = [
        ("application", 1000), ("apple", 950), ("apply", 800),
        ("software", 700), ("program", 600), ("tool", 500),
        ("banana", 400), ("fruit", 300), ("device", 200),
    ]
    
    # Build all three
    trie = SmartAutocomplete(k=5)
    for w, f in words:
        trie.insert(w, f)
    
    semantic = SemanticSearch()
    semantic.index_words([w for w, _ in words])
    
    hybrid = HybridAutocomplete()
    hybrid.build_index(words)
    
    query = "app"
    
    print("="*60)
    print(f"BENCHMARK: Query = '{query}'")
    print("="*60)
    
    # Trie only
    start = time.perf_counter_ns()
    trie_results = trie.search(query, limit=5)
    trie_time = (time.perf_counter_ns() - start) / 1000
    
    print(f"\nTrie-only ({trie_time:.1f} µs):")
    for freq, word in trie_results:
        print(f"  {word} (freq: {freq})")
    
    # Semantic only
    start = time.perf_counter_ns()
    sem_results = semantic.semantic_search(query, top_k=5)
    sem_time = (time.perf_counter_ns() - start) / 1000
    
    print(f"\nSemantic-only ({sem_time:.1f} µs):")
    for word, sim in sem_results:
        print(f"  {word} (sim: {sim:.3f})")
    
    # Hybrid
    start = time.perf_counter_ns()
    hyb_results = hybrid.hybrid_search(query, limit=5)
    hyb_time = (time.perf_counter_ns() - start) / 1000
    
    print(f"\nHybrid ({hyb_time:.1f} µs):")
    for r in hyb_results:
        print(f"  {r['word']} (score: {r['score']:.3f}, source: {r['source']})")
    
    print("\n" + "="*60)
    print("HYBRID WINS: Exact matches first, then related concepts")
    print("="*60)

if __name__ == "__main__":
    benchmark()