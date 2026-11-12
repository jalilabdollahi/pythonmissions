# Mission 138 - Sliding Window Limiter (solution)
# Count requests per key in a trailing time window using a deque.
from collections import defaultdict, deque


class SlidingWindowCounter:
    def __init__(self, window_seconds, clock):
        self.window = window_seconds
        self.clock = clock
        self._hits = defaultdict(deque)

    def _evict(self, key):
        now = self.clock()
        queue = self._hits[key]
        while queue and now - queue[0] >= self.window:
            queue.popleft()

    def hit(self, key):
        self._evict(key)
        self._hits[key].append(self.clock())

    def count(self, key):
        self._evict(key)
        return len(self._hits[key])

    def allow(self, key, limit):
        self._evict(key)
        if len(self._hits[key]) >= limit:
            return False
        self._hits[key].append(self.clock())
        return True

    def busiest(self, n=3):
        for key in list(self._hits):
            self._evict(key)
        ranked = sorted(self._hits.items(), key=lambda kv: (-len(kv[1]), kv[0]))
        return [(key, len(q)) for key, q in ranked[:n] if q]
