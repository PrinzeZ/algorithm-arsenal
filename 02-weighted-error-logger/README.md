# Project 2: Weighted Top-K Error Logger

## Trade-off Analysis

| Metric | Naive | Optimized | Winner |
|--------|-------|-----------|--------|
| Speed | 43.6s | 56.6s | Naive (C-optimized Counter) |
| Memory | 1642 MB | 22 MB | **Optimized (75× less)** |
| Time-decay | ❌ No | ✅ Yes | **Optimized** |
| Streaming | ❌ Load all | ✅ Line-by-line | **Optimized** |

## Why Optimized Is Slower on Single Machine

Python's `collections.Counter.most_common()` is written in C. Our pure-Python heap can't beat it for speed. But it **can** do things Counter cannot:
- Process infinite streams (never load all into memory)
- Time-decay: recent errors weighted higher
- Severity scoring: CRITICAL = 5× ERROR

## Production Architecture

In real systems, the optimized version runs distributed:
- Multiple stream processors (Kafka consumers)
- Each holds O(K) memory
- Aggregate results in central dashboard

Naive approach would OOM (out-of-memory) at scale.