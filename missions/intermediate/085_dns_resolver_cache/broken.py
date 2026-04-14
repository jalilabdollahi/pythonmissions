# Mission 085 - DNS Resolver Cache
# Fix the 2 bugs in this script.
import time

class DNSCache:
    def __init__(self):
        self._cache = {}  # hostname -> (ip, expiry)

    def set(self, hostname, ip, ttl):
        expiry = time.monotonic() + ttl
        self._cache[hostname] = (ip, expiry)

    def get(self, hostname):
        if hostname not in self._cache:
            return None
        ip, expiry = self._cache[hostname]
        if time.monotonic() >= expiry:  # BUG 1: should be > expiry (expired strictly after)
            del self._cache[hostname]
            return None
        return ip

    def cleanup(self):
        """Remove all expired entries."""
        now = time.monotonic()
        # BUG 2: modifying dict while iterating
        for host, (ip, expiry) in self._cache.items():
            if now > expiry:
                del self._cache[host]
