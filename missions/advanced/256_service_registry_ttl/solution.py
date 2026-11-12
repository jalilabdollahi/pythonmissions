# Mission 256 - Service Registry (solution)
# In-memory service registry: instances register, heartbeat, expire and deregister.


class Instance:
    def __init__(self, instance_id, address, ttl, now, tags=()):
        self.id = instance_id
        self.address = address
        self.ttl = ttl
        self.tags = frozenset(tags)
        self.registered_at = now
        self.expires_at = now + ttl

    def alive(self, now):
        return now < self.expires_at


class Registry:
    def __init__(self, clock, default_ttl=30.0):
        self._clock = clock
        self.default_ttl = default_ttl
        self._services = {}
        self.events = []

    def register(self, service, instance_id, address, ttl=None, tags=()):
        now = self._clock()
        ttl = self.default_ttl if ttl is None else ttl
        if ttl <= 0:
            raise ValueError("ttl must be positive")
        entries = self._services.setdefault(service, [])
        entries[:] = [e for e in entries if e.id != instance_id]
        entries.append(Instance(instance_id, address, ttl, now, tags))
        self.events.append(("up", service, instance_id))

    def _find(self, service, instance_id):
        for entry in self._services.get(service, []):
            if entry.id == instance_id:
                return entry
        return None

    def heartbeat(self, service, instance_id):
        """Extend the lease. An unknown or already expired instance must re-register."""
        entry = self._find(service, instance_id)
        if entry is None:
            return False
        now = self._clock()
        if not entry.alive(now):
            self._drop(service, entry, "expired")
            return False
        entry.expires_at = now + entry.ttl
        return True

    def deregister(self, service, instance_id):
        entry = self._find(service, instance_id)
        if entry is None:
            return False
        self._drop(service, entry, "down")
        return True

    def _drop(self, service, entry, reason):
        self._services[service].remove(entry)
        self.events.append((reason, service, entry.id))

    def sweep(self):
        now = self._clock()
        expired = []
        for service, entries in self._services.items():
            for entry in [e for e in entries if not e.alive(now)]:
                self._drop(service, entry, "expired")
                expired.append((service, entry.id))
        return sorted(expired)

    def lookup(self, service, tag=None):
        now = self._clock()
        live = [e for e in self._services.get(service, []) if e.alive(now)]
        if tag is not None:
            live = [e for e in live if tag in e.tags]
        return sorted(e.address for e in live)

    def services(self):
        now = self._clock()
        return sorted(name for name, entries in self._services.items() if any(e.alive(now) for e in entries))

    def ttl_remaining(self, service, instance_id):
        entry = self._find(service, instance_id)
        if entry is None:
            return None
        return max(0.0, entry.expires_at - self._clock())
