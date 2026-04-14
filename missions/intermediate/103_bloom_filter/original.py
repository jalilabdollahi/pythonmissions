# Mission 103 - Bloom Filter
# Fix the 2 bugs in this script.
import hashlib

class BloomFilter:
    def __init__(self, size=1000, num_hashes=3):
        self.size = size
        self.num_hashes = num_hashes
        self.bits = [0] * size

    def _hashes(self, item):
        """Generate num_hashes different hash indices."""
        result = []
        for i in range(self.num_hashes):
            h = hashlib.md5(f"{item}".encode()).hexdigest()  # BUG 1: same hash every time, no seed
            result.append(int(h, 16) % self.size)
        return result

    def add(self, item):
        for idx in self._hashes(item):
            self.bits[idx] = 1

    def might_contain(self, item):
        return any(self.bits[idx] for idx in self._hashes(item))  # BUG 2: should be all(), not any()
