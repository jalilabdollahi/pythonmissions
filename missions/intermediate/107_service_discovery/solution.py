# Mission 107 - Service Discovery Registry
# Fixed solution
import time

class ServiceRegistry:
    def __init__(self):
        self._services = {}

    def register(self, name, host, port, ttl=30):
        if name not in self._services:
            self._services[name] = []
        # Remove existing entry for same host:port
        self._services[name] = [
            i for i in self._services[name]
            if not (i["host"] == host and i["port"] == port)
        ]
        entry = {"host": host, "port": port, "expires": time.monotonic() + ttl}
        self._services[name].append(entry)

    def lookup(self, name):
        instances = self._services.get(name, [])
        now = time.monotonic()
        alive = [i for i in instances if i["expires"] > now]
        return [(i["host"], i["port"]) for i in alive]

    def deregister(self, name, host, port):
        if name in self._services:
            self._services[name] = [
                i for i in self._services[name]
                if not (i["host"] == host and i["port"] == port)
            ]
