# Mission 151 - Expiring Lookups (solution)
# A small time-to-live cache whose notion of "now" is injected.


class TTLCache:
    def __init__(self, ttl, clock):
        self.ttl = ttl
        self.clock = clock
        self._items = {}

    def _expired(self, stamp):
        return self.clock() - stamp >= self.ttl

    def set(self, key, value):
        self._items[key] = (value, self.clock())

    def get(self, key, default=None):
        entry = self._items.get(key)
        if entry is None:
            return default
        value, stamp = entry
        if self._expired(stamp):
            del self._items[key]
            return default
        return value

    def purge(self):
        dead = [k for k, (_, stamp) in self._items.items() if self._expired(stamp)]
        for key in dead:
            del self._items[key]
        return len(dead)

    def size(self):
        self.purge()
        return len(self._items)

    def get_or_load(self, key, loader):
        value = self.get(key)
        if value is None:
            value = loader()
            self.set(key, value)
        return value
