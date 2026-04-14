# Mission 122 - Idempotency Key Manager
# Fixed solution
import time

class IdempotencyManager:
    def __init__(self, ttl=3600):
        self.ttl = ttl
        self._store = {}

    def _normalize(self, key):
        return key.lower()

    def set(self, key, result):
        normalized = self._normalize(key)
        self._store[normalized] = {
            "result": result,
            "expires": time.monotonic() + self.ttl,
        }

    def get(self, key):
        normalized = self._normalize(key)
        entry = self._store.get(normalized)
        if entry is None:
            return None
        if time.monotonic() > entry["expires"]:
            del self._store[normalized]
            return None
        return entry["result"]

    def is_duplicate(self, key):
        return self.get(key) is not None
