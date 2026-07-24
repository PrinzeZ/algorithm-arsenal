from collections import Counter
import time

def naive_top_errors(log_file, k=10):
    with open(log_file, 'r') as f:
        lines = f.readlines()
    
    errors = []
    for line in lines:
        if "ERROR" in line or "CRITICAL" in line:
            # Find the actual message after the level
            if "ERROR:" in line:
                msg = line.split("ERROR:", 1)[1].strip()
            elif "CRITICAL:" in line:
                msg = line.split("CRITICAL:", 1)[1].strip()
            else:
                msg = line.strip()
            errors.append(msg)
    
    return Counter(errors).most_common(k)

if __name__ == "__main__":
    with open("test.log", "w") as f:
        for i in range(100000):
            f.write(f"2024-07-21 10:00:00 ERROR: Database timeout\n")
            f.write(f"2024-07-21 10:00:01 CRITICAL: Server crash\n")
            f.write(f"2024-07-21 10:00:02 INFO: All good\n")
    
    start = time.time()
    print(naive_top_errors("test.log", 5))
    print(f"Time: {time.time() - start:.4f}s")