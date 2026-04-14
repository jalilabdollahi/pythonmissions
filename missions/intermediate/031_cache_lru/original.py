# Mission 031 - LRU Cache Implementation
# Fix the 2 bugs in this script.
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=True)  # BUG 1: should be last=False (evict oldest)

    def size(self):
        return len(self.cache) - 1  # BUG 2: spurious -1
