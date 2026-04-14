# Mission 108 - Distributed Lock
# Fixed solution
import threading
import time

class DistributedLock:
    def __init__(self, name, ttl=30):
        self.name = name
        self.ttl = ttl
        self._holder = None
        self._expires = 0
        self._mutex = threading.Lock()

    def acquire(self, owner, timeout=10):
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            now = time.monotonic()
            with self._mutex:
                if self._holder is None or now > self._expires:
                    self._holder = owner
                    self._expires = now + self.ttl
                    return True
            time.sleep(0.01)
        return False

    def release(self, owner):
        with self._mutex:
            if self._holder == owner:
                self._holder = None
                return True
        return False

    def is_locked(self):
        with self._mutex:
            return self._holder is not None and time.monotonic() < self._expires
