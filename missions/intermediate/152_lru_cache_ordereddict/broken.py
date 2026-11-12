# Mission 152 - Least Recently Used
# An in-memory LRU cache built on OrderedDict.
from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity):
        if capacity < 1:
            raise ValueError("capacity must be at least 1")
        self.capacity = capacity
        self._data = OrderedDict()
        self.evictions = 0

    def get(self, key):
        if key not in self._data:
            return None
        return self._data[key]

    def put(self, key, value):
        self._data[key] = value
        if len(self._data) > self.capacity:
            self._data.popitem(last=True)
            self.evictions += 1

    def keys(self):
        return list(self._data)

    def __len__(self):
        return len(self._data)

    def __contains__(self, key):
        return key in self._data
