# Mission 006 (Advanced) - Distributed Rate Limiter
# Fix the 2 bugs in this script.
import time

class FakeRedis:
    """Test stub for Redis."""
    def __init__(self): self._store = {}; self._expiry = {}
    def incr(self, key):
        self._store[key] = self._store.get(key, 0) + 1
        return self._store[key]
    def expire(self, key, seconds):
        self._expiry[key] = time.monotonic() + seconds
    def get(self, key):
        if key in self._expiry and time.monotonic() > self._expiry[key]:
            del self._store[key]; del self._expiry[key]
        return self._store.get(key, 0)

class DistributedRateLimiter:
    def __init__(self, redis_client, limit, window_seconds):
        self.redis = redis_client
        self.limit = limit
        self.window = window_seconds

    def _window_key(self, identifier):
        window = int(time.time() // self.window)
        return f"ratelimit:{identifier}"  # BUG 1: should include window in key

    def is_allowed(self, identifier):
        key = self._window_key(identifier)
        count = self.redis.incr(key)
        if count == 1:
            self.redis.expire(key, self.limit)  # BUG 2: should expire after window_seconds not limit
        return count <= self.limit

    def remaining(self, identifier):
        key = self._window_key(identifier)
        used = int(self.redis.get(key))
        return max(0, self.limit - used)
