# Mission 020 (Advanced) - Object Pool Allocator
# Fixed solution
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
        self._local = threading.local()
        self._size = size

    def _get_pool(self):
        if not hasattr(self._local, "pool"):
            self._local.pool = [self.factory() for _ in range(self._size)]
        return self._local.pool

    def acquire(self):
        pool = self._get_pool()
        if pool:
            return pool.pop()
        return self.factory()

    def release(self, obj):
        obj.reset()
        pool = self._get_pool()
        if len(pool) < self._size:
            pool.append(obj)
