"""
NAIVE RATE LIMITER
Stores every request timestamp. Memory grows forever.
"""

import time

class NaiveRateLimiter:
    def __init__(self, max_requests=5, window=60):
        self.max_requests = max_requests
        self.window = window
        self.requests = []  # ALL timestamps stored
    
    def is_allowed(self, user_id):
        now = time.time()
        # Clean old requests: O(N) every call!
        self.requests = [t for t in self.requests if now - t < self.window]
        
        if len(self.requests) < self.max_requests:
            self.requests.append(now)
            return True
        return False


if __name__ == "__main__":
    limiter = NaiveRateLimiter(max_requests=3, window=10)
    for i in range(5):
        result = limiter.is_allowed("user1")
        print(f"Request {i}: {'ALLOWED' if result else 'BLOCKED'}")
        time.sleep(1)