import heapq
import time
import math

class ErrorEntry:
    def __init__(self, message, severity=1.0):
        self.message = message
        self.count = 1
        self.severity = severity
        self.last_seen = time.time()
    
    def calc_score(self):
        """Recalculate score at call time (for decay)"""
        minutes_ago = (time.time() - self.last_seen) / 60
        return self.count * self.severity * math.exp(-0.1 * minutes_ago)
    
    def update(self, severity=1.0):
        self.count += 1
        self.severity = max(self.severity, severity)
        self.last_seen = time.time()
    
    def __lt__(self, other):
        return self.calc_score() < other.calc_score()


class SmartErrorLogger:
    def __init__(self, k=10):
        self.k = k
        self.errors = {}
        self.heap = []
    
    def process_line(self, line, severity=1.0):
        if "ERROR" not in line and "CRITICAL" not in line:
            return
        
        if "ERROR:" in line:
            msg = line.split("ERROR:", 1)[1].strip()
        elif "CRITICAL:" in line:
            msg = line.split("CRITICAL:", 1)[1].strip()
            severity = 5.0
        else:
            return
        
        if msg in self.errors:
            self.errors[msg].update(severity)
        else:
            self.errors[msg] = ErrorEntry(msg, severity)
    
    def get_top_k(self):
        """Recalculate all scores, then heapq top K"""
        all_entries = list(self.errors.values())
        return heapq.nlargest(self.k, all_entries, key=lambda e: e.calc_score())
    
    def process_file(self, filepath):
        with open(filepath, 'r') as f:
            for line in f:
                self.process_line(line.strip())
    
    def report(self):
        print(f"\n{'='*50}")
        print(f"TOP {self.k} ERRORS (Time-Decayed & Severity-Weighted)")
        print(f"{'='*50}")
        for i, e in enumerate(self.get_top_k(), 1):
            print(f"{i}. {e.message}")
            print(f"   Count: {e.count} | Severity: {e.severity}")
            print(f"   Score: {e.calc_score():.2f}")
            print()


if __name__ == "__main__":
    import time as t
    
    logger = SmartErrorLogger(k=5)
    
    print("Simulating real-time error stream...")
    
    logger.process_line("2024-07-21 10:00:00 ERROR: Database timeout", severity=1.0)
    logger.process_line("2024-07-21 10:00:01 ERROR: Database timeout", severity=1.0)
    logger.process_line("2024-07-21 10:00:02 CRITICAL: Server crash", severity=5.0)
    
    print("\nInitial state:")
    logger.report()
    
    t.sleep(2)
    logger.process_line("2024-07-21 10:02:00 ERROR: Database timeout", severity=1.0)
    logger.process_line("2024-07-21 10:02:01 ERROR: Null pointer", severity=1.0)
    
    print("After 2 seconds:")
    logger.report()
    
    t.sleep(5)
    logger.process_line("2024-07-21 10:07:00 WARNING: Slow query", severity=0.5)
    
    print("After 7 seconds:")
    logger.report()