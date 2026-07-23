# ⚡ Algorithm Arsenal

Real-world algorithms optimized for production. Each project includes:
- **Naive implementation** (what NOT to do)
- **Optimized implementation** (production-ready)
- **Benchmarks** (proof of speedup)

---

## 📁 Project 1: Smart Autocomplete

**Real-world use:** Search engines, IDE command palettes, command-line tools

### The Problem
Given a dictionary of 100,000+ words, find all words starting with a user-typed prefix.

### Naive Approach
Linear scan through entire list. **O(N × M)** time.

### Optimized Approach: Trie + Frequency Ranking
- **Trie (Prefix Tree)** for O(M) prefix lookup
- **Eager indexing** — words pre-stored at every node
- **Frequency ranking** — popular words surface first

### Benchmark Results

| Prefix | Matches | Naive Time | Trie Time | Speedup |
|--------|---------|-----------|-----------|---------|
| `word999` | 1 | 9.25s | 0.009s | **1026x** |
| `word1` | ~1000 | 9.63s | 0.70s | **14x** |
| `word` | ~10000 | 11.97s | 8.43s | **1x** |

*Note: At 10K+ matches, Python's sorting becomes the bottleneck. Production systems use heaps or pre-sorted structures to maintain sub-millisecond latency.*

### Tech Stack
- Python 3.11+
- Data Structures: Trie, Hash Map
- Algorithms: Prefix matching, frequency-based ranking

---

## 🚀 How to Run

```bash
cd 01-smart-autocomplete
python naive.py
python optimized.py
python benchmark.py

### Hybrid Semantic Search (NEW)

Combines Trie lexical matching with vector embeddings for meaning-based search.

**Architecture:**
- **Trie Layer:** O(M) prefix matching (letters)
- **Semantic Layer:** Cosine similarity on 384-dim vectors (meaning)
- **Merge Layer:** Weighted scoring (60% lexical + 40% semantic)

**Example:**

Query: "app"
Trie: ["application", "apple", "apply"]
Semantic: ["software", "program", "tool"]
Hybrid: ["application", "apple", "software", "apply", "program"]


**Files:** `semantic_layer.py`, `hybrid_search.py`, `hybrid_benchmark.py`

### Performance Benchmarks

| Prefix | Matches | Naive Time | Trie Time | Speedup |
|--------|---------|-----------|-----------|---------|
| `word999` | 1 | 7.69s | 0.0005s | **15,240x** |
| `word1` | ~1000 | 7.50s | 0.0010s | **7,491x** |
| `word` | ~10000 | 9.55s | 0.0014s | **6,993x** |

*Trie uses min-heap pre-computation: O(M) search time regardless of dictionary size.*

### Massive Scale Performance

Tested on 10 million words:

| Prefix | Matches | Time |
|--------|---------|------|
| `word9999999` | 1 | ~1ms |
| `word9` | ~10,000 | <1ms |
| `word` | ~10,000,000 | <1ms |

Trie search time is O(M) where M = prefix length. Dictionary size is irrelevant.