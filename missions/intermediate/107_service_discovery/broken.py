# Mission 107 - Service Discovery Registry
# Fix the 2 bugs in this script.
import time

class ServiceRegistry:
    def __init__(self):
        self._services = {}  # name -> list of {host, port, expires}

    def register(self, name, host, port, ttl=30):
        if name not in self._services:
            self._services[name] = []
        entry = {"host": host, "port": port, "expires": time.monotonic() + ttl}
        self._services[name].append(entry)  # BUG 1: should replace existing (host,port) entry if present

    def lookup(self, name):
        """Return list of (host, port) for healthy instances."""
        instances = self._services.get(name, [])
        now = time.monotonic()
        alive = [i for i in instances if i["expires"] < now]  # BUG 2: logic inverted — should be > now
        return [(i["host"], i["port"]) for i in alive]

    def deregister(self, name, host, port):
        if name in self._services:
            self._services[name] = [
                i for i in self._services[name]
                if not (i["host"] == host and i["port"] == port)
            ]
