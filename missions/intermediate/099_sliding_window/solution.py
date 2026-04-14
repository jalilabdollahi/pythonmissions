# Mission 099 - Sliding Window Rate Counter
# Fixed solution
from collections import deque
import time

class SlidingWindow:
    def __init__(self, window_seconds=60):
        self.window = window_seconds
        self._timestamps = deque()

    def record(self):
        self._timestamps.append(time.monotonic())

    def _evict_old(self):
        cutoff = time.monotonic() - self.window
        while self._timestamps and self._timestamps[0] < cutoff:
            self._timestamps.popleft()

    def count(self):
        self._evict_old()
        return len(self._timestamps)
