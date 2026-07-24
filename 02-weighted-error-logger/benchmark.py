import time
import random
import tracemalloc
from naive import naive_top_errors
from optimized import SmartErrorLogger

print("Creating 10M lines with 100,000 unique errors...")

error_types = [f"ErrorType{i}" for i in range(100000)]

with open("massive.log", "w") as f:
    for i in range(10000000):
        err = random.choice(error_types)
        level = "CRITICAL" if i % 500 == 0 else "ERROR"
        f.write(f"2024-07-21 10:00:00 {level}: {err}\n")

# NAIVE: Memory + Time
tracemalloc.start()
start = time.time()
naive_result = naive_top_errors("massive.log", 10)
naive_time = time.time() - start
naive_mem = tracemalloc.get_traced_memory()[1] / (1024*1024)  # MB
tracemalloc.stop()

print(f"\nNaive: {naive_time:.2f}s, Memory: {naive_mem:.1f}MB")

# OPTIMIZED: Memory + Time
tracemalloc.start()
logger = SmartErrorLogger(k=10)
start = time.time()
logger.process_file("massive.log")
opt_time = time.time() - start
opt_mem = tracemalloc.get_traced_memory()[1] / (1024*1024)  # MB
tracemalloc.stop()

print(f"Optimized: {opt_time:.2f}s, Memory: {opt_mem:.1f}MB")

print(f"\nSpeedup: {naive_time/opt_time:.1f}x")
print(f"Memory reduction: {naive_mem/opt_mem:.1f}x less memory")