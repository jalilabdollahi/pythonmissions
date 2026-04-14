# Mission 103 - Bloom Filter
# Fixed solution
import hashlib

class BloomFilter:
    def __init__(self, size=1000, num_hashes=3):
        self.size = size
        self.num_hashes = num_hashes
        self.bits = [0] * size

    def _hashes(self, item):
        result = []
        for i in range(self.num_hashes):
            h = hashlib.md5(f"{i}:{item}".encode()).hexdigest()
            result.append(int(h, 16) % self.size)
        return result

    def add(self, item):
        for idx in self._hashes(item):
            self.bits[idx] = 1

    def might_contain(self, item):
        return all(self.bits[idx] for idx in self._hashes(item))
