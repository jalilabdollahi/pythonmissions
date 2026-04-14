# Mission 085 - DNS Resolver Cache
# Fixed solution
import time

class DNSCache:
    def __init__(self):
        self._cache = {}

    def set(self, hostname, ip, ttl):
        expiry = time.monotonic() + ttl
        self._cache[hostname] = (ip, expiry)

    def get(self, hostname):
        if hostname not in self._cache:
            return None
        ip, expiry = self._cache[hostname]
        if time.monotonic() > expiry:
            del self._cache[hostname]
            return None
        return ip

    def cleanup(self):
        now = time.monotonic()
        expired = [h for h, (_, exp) in self._cache.items() if now > exp]
        for host in expired:
            del self._cache[host]
