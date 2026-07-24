# Project 3: Concurrent Web Crawler

## The Problem
Crawling websites one URL at a time is slow. Most time is spent waiting for network responses.

## Naive Approach
Sequential requests. Time = N × latency.

## Optimized Approach
ThreadPool with 5 workers, deduplication, politeness delay.

## Benchmark

| Metric | Naive | Optimized | Speedup |
|--------|-------|-----------|---------|
| 10 URLs | 14.36s | 1.80s | **8x** |

## Features
- **Parallelism:** ThreadPoolExecutor with configurable workers
- **Deduplication:** `seen` set prevents redundant fetches
- **Politeness:** 0.5s delay between requests (don't hammer servers)
- **Timeout:** 5s max per request

## Production Additions (Not Implemented)
- robots.txt respect
- User-agent rotation
- Retry with exponential backoff
- Distributed crawling (multiple machines)