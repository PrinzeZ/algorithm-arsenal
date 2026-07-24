\# Project 1: Smart Autocomplete



\## Benchmarks



| Prefix | Dictionary Size | Naive | Trie | Speedup |

|--------|----------------|-------|------|---------|

| `word999` | 10M | 7.69s | 0.0005s | \*\*15,240x\*\* |

| `word1` | 10M | 7.50s | 0.0010s | \*\*7,491x\*\* |

| `word` | 10M | 9.55s | 0.0014s | \*\*6,993x\*\* |



Trie: O(M) where M = prefix length. Dictionary size irrelevant.



\## Files

\- `naive.py` — Linear scan

\- `optimized.py` — Trie with min-heap

\- `benchmark.py` — Performance comparison

\- `massive\_benchmark.py` — 10M word test

\- `semantic\_layer.py` — Vector embeddings

\- `hybrid\_search.py` — Trie + semantic merge

