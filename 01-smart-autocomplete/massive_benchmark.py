"""
Massive Scale Benchmark: 10 Million Words
Tests Trie performance at extreme scale
"""

import time
from optimized import SmartAutocomplete

def massive_benchmark():
    print("=" * 60)
    print("MASSIVE SCALE BENCHMARK")
    print("=" * 60)
    
    # Generate 10 million words: word0, word1, ..., word9999999
    total_words = 10_000_000
    print(f"\nGenerating {total_words:,} words...")
    
    # We can't store all in RAM as a list, so generate on the fly for Trie
    trie = SmartAutocomplete(k=5)
    
    print(f"Inserting {total_words:,} words into Trie...")
    start = time.time()
    
    for i in range(total_words):
        word = f"word{i}"
        freq = total_words - i  # word0 has highest frequency
        trie.insert(word, freq)
        
        if i % 1_000_000 == 0 and i > 0:
            print(f"  Inserted {i:,} words...")
    
    insert_time = time.time() - start
    print(f"Insert complete: {insert_time:.2f}s")
    
    # Test searches
    tests = [
        ("word9999999", "1 match (last word)"),
        ("word9999", "~10 matches"),
        ("word999", "~100 matches"),
        ("word99", "~1000 matches"),
        ("word9", "~10000 matches"),
        ("word", "~10 million matches"),
    ]
    
    print("\n" + "=" * 60)
    print("SEARCH BENCHMARKS")
    print("=" * 60)
    
    for prefix, desc in tests:
        start = time.time()
        results = trie.search(prefix, limit=5)
        search_time = time.time() - start
        
        print(f"\nPrefix: '{prefix}' ({desc})")
        print(f"  Time: {search_time:.6f}s ({search_time * 1000:.3f}ms)")
        print(f"  Results: {results[:3]}...")

if __name__ == "__main__":
    massive_benchmark()