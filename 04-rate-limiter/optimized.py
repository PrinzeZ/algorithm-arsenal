"""
OPTIMIZED RATE LIMITER
Sliding window with deque. O(1) operations, bounded memory.
"""

import time
from collections import deque

class SmartRateLimiter:
    def __init__(self, max_requests=5, window=60):
        self.max_requests = max_requests
        self.window = window
        self.users = {}  # user_id -> deque of timestamps
    
    def is_allowed(self, user_id):
        now = time.time()
        
        if user_id not in self.users:
            self.users[user_id] = deque()
        
        user_queue = self.users[user_id]
        
        # Remove old requests outside window: O(1) amortized
        while user_queue and now - user_queue[0] > self.window:
            user_queue.popleft()
        
        if len(user_queue) < self.max_requests:
            user_queue.append(now)
            return True
        return False
    
    def get_remaining(self, user_id):
        if user_id not in self.users:
            return self.max_requests
        return self.max_requests - len(self.users[user_id])


if __name__ == "__main__":
    limiter = SmartRateLimiter(max_requests=3, window=10)
    for i in range(5):
        result = limiter.is_allowed("user1")
        remaining = limiter.get_remaining("user1")
        print(f"Request {i}: {'ALLOWED' if result else 'BLOCKED'} (remaining: {remaining})")
        time.sleep(1)