import time
from naive import naive_search
from optimized import SmartAutocomplete

print("Creating test data...")
all_words = [f"word{i}" for i in range(100000)]
all_words.extend(["apple", "application", "apply", "appetizer"])

# Build the Trie once
trie = SmartAutocomplete()
for w in all_words:
    trie.insert(w, 1)

def benchmark(prefix, name):
    print(f"\n--- Testing prefix: '{prefix}' ({name}) ---")
    
    # Naive
    start = time.time()
    for _ in range(1000):  # Run 1000 times for better measurement
        naive_search(all_words, prefix)
    naive_time = time.time() - start
    
    # Trie
    start = time.time()
    for _ in range(1000):
        trie.search(prefix)
    trie_time = time.time() - start
    
    print(f"Naive:  {naive_time:.4f}s")
    print(f"Trie:   {trie_time:.4f}s")
    
    if trie_time > 0:
        speedup = naive_time / trie_time
        print(f"Speedup: {speedup:.0f}x faster!")
    else:
        print("Speedup: So fast it rounded to 0!")

# Test 1: Prefix with 1 match (the original)
benchmark("word999", "1 match")

# Test 2: Prefix with ~1000 matches (where Trie DOMINATES)
benchmark("word1", "~1000 matches")

# Test 3: Prefix with ~10000 matches
benchmark("word", "~10000 matches")