# Project 4: API Rate Limiter

## The Problem
Prevent users from overwhelming your API with too many requests.

## Naive Approach
Store every request timestamp in a list. Clean old ones on every check.
- Time: O(N) per check (scans all timestamps)
- Space: O(total requests) — grows forever

## Optimized Approach
Sliding window with deque per user. Drop expired timestamps instantly.
- Time: O(1) amortized per check
- Space: O(window limit) — constant

## Benchmark

| Metric | Naive | Optimized | Speedup |
|--------|-------|-----------|---------|
| 1M requests | 0.43s | 0.02s | **25.9x** |

## Features
- Per-user tracking (isolated quotas)
- O(1) check and update
- Configurable window and limit
- Returns remaining quota

## Real-World Use
- Stripe API: 100 requests/second
- GitHub API: 5000 requests/hour
- Twitter API: 300 tweets/3 hours