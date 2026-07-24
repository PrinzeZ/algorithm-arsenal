import time
from naive import NaiveRateLimiter
from optimized import SmartRateLimiter

print("="*50)
print("RATE LIMITER BENCHMARK")
print("="*50)

# Simulate 1 million requests over time
num_requests = 1000000

# Naive
naive = NaiveRateLimiter(max_requests=100, window=60)
start = time.time()
for i in range(num_requests):
    naive.is_allowed("user1")
naive_time = time.time() - start

# Optimized
smart = SmartRateLimiter(max_requests=100, window=60)
start = time.time()
for i in range(num_requests):
    smart.is_allowed("user1")
smart_time = time.time() - start

print(f"\nNaive:     {naive_time:.4f}s")
print(f"Optimized: {smart_time:.4f}s")
print(f"Speedup:   {naive_time/smart_time:.1f}x")

print(f"\nNaive stored:     {len(naive.requests):,} timestamps (grows forever)")
print(f"Optimized stored: {len(smart.users.get('user1', [])):,} timestamps (bounded by window)")

# The real test: memory after 1M requests
print(f"\nNaive memory: ~{len(naive.requests) * 8 / 1024:.1f} KB (just timestamps)")
print(f"Optimized memory: ~{len(smart.users.get('user1', [])) * 8 / 1024:.1f} KB")