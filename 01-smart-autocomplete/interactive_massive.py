"""
Interactive Massive Trie Test
Type any prefix, see instant results
"""

import time
import random
import string
from optimized import SmartAutocomplete

def generate_random_word(length=8):
    """Generate random lowercase word"""
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def main():
    print("=" * 60)
    print("INTERACTIVE MASSIVE TRIE TEST")
    print("=" * 60)
    
    # Start with 10 million (adjust based on your RAM)
    total_words = 10_000_000
    
    print(f"\nGenerating {total_words:,} RANDOM words...")
    
    trie = SmartAutocomplete(k=5)
    
    start = time.time()
    for i in range(total_words):
        # Mix of random words + some real-ish words
        if i % 1000 == 0:
            word = f"app{random.randint(0, 9999)}"
        elif i % 1000 == 1:
            word = f"test{random.randint(0, 9999)}"
        else:
            word = generate_random_word(6)
        
        freq = random.randint(1, 1000000)
        trie.insert(word, freq)
        
        if i % 1_000_000 == 0 and i > 0:
            elapsed = time.time() - start
            print(f"  Inserted {i:,} words... ({elapsed:.1f}s)")
    
    insert_time = time.time() - start
    print(f"\nDone! Inserted {total_words:,} words in {insert_time:.1f}s")
    print(f"Type a prefix and hit Enter. Type 'quit' to exit.\n")
    
    # Interactive loop
    while True:
        prefix = input("Enter prefix: ").strip().lower()
        
        if prefix == 'quit':
            print("Goodbye!")
            break
        
        if not prefix:
            continue
        
        # Search
        search_start = time.perf_counter_ns()
        results = trie.search(prefix, limit=5)
        search_end = time.perf_counter_ns()
        
        search_us = (search_end - search_start) / 1000  # microseconds
        
        print(f"\n  Results for '{prefix}' ({search_us:.1f} µs):")
        if results:
            for freq, word in results:
                print(f"    {word} (freq: {freq})")
        else:
            print("    No matches")
        print()

if __name__ == "__main__":
    main()