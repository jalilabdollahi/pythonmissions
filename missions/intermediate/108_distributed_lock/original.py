# Mission 108 - Distributed Lock
# Fix the 2 bugs in this script.
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
            if self._holder is None or now > self._expires:  # BUG 1: not protected by mutex
                self._holder = owner
                self._expires = now + self.ttl
                return True
            time.sleep(0.01)
        return False

    def release(self, owner):
        if self._holder == owner:  # BUG 2: not protected by mutex
            self._holder = None
            return True
        return False

    def is_locked(self):
        with self._mutex:
            return self._holder is not None and time.monotonic() < self._expires
