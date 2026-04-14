# Mission 105 - Alert Deduplicator
# Fix the 2 bugs in this script.
import time
import hashlib
import json

class AlertDeduplicator:
    def __init__(self, ttl=300):
        self.ttl = ttl
        self._seen = {}  # fingerprint -> expiry

    def _fingerprint(self, alert):
        data = json.dumps({"name": alert["name"], "labels": alert.get("labels", {})})
        return hashlib.md5(data.encode()).hexdigest()  # BUG 1: dict order not guaranteed — sort keys

    def _evict_expired(self):
        now = time.monotonic()
        expired = [k for k, exp in self._seen.items() if now > exp]
        for k in expired:
            del self._seen[k]

    def is_duplicate(self, alert):
        # BUG 2: should evict expired entries before checking
        fp = self._fingerprint(alert)
        if fp in self._seen:
            return True
        self._seen[fp] = time.monotonic() + self.ttl
        return False
