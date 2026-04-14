# Mission 105 - Alert Deduplicator
# Fixed solution
import time
import hashlib
import json

class AlertDeduplicator:
    def __init__(self, ttl=300):
        self.ttl = ttl
        self._seen = {}

    def _fingerprint(self, alert):
        data = json.dumps({"name": alert["name"], "labels": alert.get("labels", {})}, sort_keys=True)
        return hashlib.md5(data.encode()).hexdigest()

    def _evict_expired(self):
        now = time.monotonic()
        expired = [k for k, exp in self._seen.items() if now > exp]
        for k in expired:
            del self._seen[k]

    def is_duplicate(self, alert):
        self._evict_expired()
        fp = self._fingerprint(alert)
        if fp in self._seen:
            return True
        self._seen[fp] = time.monotonic() + self.ttl
        return False
