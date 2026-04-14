# Mission 020 (Advanced) - Object Pool Allocator
# Fix the 2 bugs in this script.
import threading

class PooledMetric:
    def __init__(self):
        self.name = ""
        self.value = 0.0
        self.tags = {}
    def reset(self):
        self.name = ""; self.value = 0.0; self.tags = {}

class ObjectPool:
    def __init__(self, factory, size=100):
        self.factory = factory
        self.size = size
        self._pool = [factory() for _ in range(size)]
        self._lock = threading.Lock()  # BUG 1: should use threading.local() for per-thread pool

    def acquire(self):
        with self._lock:
            if self._pool:
                return self._pool.pop()
            raise RuntimeError("Pool exhausted")  # BUG 2: create new object when exhausted

    def release(self, obj):
        obj.reset()
        with self._lock:
            if len(self._pool) < self.size:
                self._pool.append(obj)
