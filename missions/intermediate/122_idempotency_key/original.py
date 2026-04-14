# Mission 122 - Idempotency Key Manager
# Fix the 2 bugs in this script.
import time

class IdempotencyManager:
    def __init__(self, ttl=3600):
        self.ttl = ttl
        self._store = {}  # key -> {result, expires}

    def _normalize(self, key):
        return key  # BUG 1: should return key.lower()

    def set(self, key, result):
        normalized = self._normalize(key)
        self._store[normalized] = {
            "result": result,
            "expires": time.monotonic() + self.ttl,
        }

    def get(self, key):
        normalized = self._normalize(key)
        # BUG 2: should check expiry and remove if expired
        entry = self._store.get(normalized)
        if entry is None:
            return None
        return entry["result"]

    def is_duplicate(self, key):
        return self.get(key) is not None
