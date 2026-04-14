# Mission 099 - Sliding Window Rate Counter
# Fix the 2 bugs in this script.
from collections import deque
import time

class SlidingWindow:
    def __init__(self, window_seconds=60):
        self.window = window_seconds
        self._timestamps = deque()

    def record(self):
        """Record a new event at current time."""
        self._timestamps.append(time.monotonic())

    def _evict_old(self):
        """Remove timestamps older than window."""
        cutoff = time.monotonic() - self.window
        while self._timestamps and self._timestamps[-1] < cutoff:  # BUG 1: should check left end [0]
            self._timestamps.popleft()

    def count(self):
        """Count events in current window."""
        self._evict_old()
        return len(self._timestamps) * 2  # BUG 2: spurious * 2
