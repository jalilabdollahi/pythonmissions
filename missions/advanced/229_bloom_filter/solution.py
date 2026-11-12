# Mission 229 - Seen-Hash Bloom Gate (solution)
# Bloom filter with textbook sizing and double hashing, used to pre-screen scan IDs.
import hashlib
import math


def optimal_bits(n, p):
    return math.ceil(-n * math.log(p) / (math.log(2) ** 2))


def optimal_hashes(m, n):
    return max(1, round(m / n * math.log(2)))


class BloomFilter:
    def __init__(self, expected_items, fp_rate):
        if expected_items <= 0 or not 0 < fp_rate < 1:
            raise ValueError("need expected_items > 0 and 0 < fp_rate < 1")
        self.expected_items = expected_items
        self.m = optimal_bits(expected_items, fp_rate)
        self.k = optimal_hashes(self.m, expected_items)
        self.bits = bytearray((self.m + 7) // 8)
        self.count = 0

    def _positions(self, item):
        digest = hashlib.sha256(item.encode("utf-8")).digest()
        h1 = int.from_bytes(digest[:8], "big")
        h2 = int.from_bytes(digest[8:16], "big") | 1
        return [(h1 + i * h2) % self.m for i in range(self.k)]

    def add(self, item):
        for pos in self._positions(item):
            self.bits[pos // 8] |= 1 << (pos % 8)
        self.count += 1

    def contains(self, item):
        return all(self.bits[pos // 8] & (1 << (pos % 8)) for pos in self._positions(item))

    def union(self, other):
        if (self.m, self.k) != (other.m, other.k):
            raise ValueError("filters must share size and hash count to be merged")
        merged = BloomFilter(self.expected_items, 0.5)
        merged.m, merged.k = self.m, self.k
        merged.bits = bytearray(a | b for a, b in zip(self.bits, other.bits))
        merged.count = self.count + other.count
        return merged

    def bits_set(self):
        return sum(bin(byte).count("1") for byte in self.bits)

    def estimated_fp_rate(self):
        fill = 1 - math.exp(-self.k * self.count / self.m)
        return fill ** self.k

    def fill_ratio(self):
        return self.bits_set() / self.m


def capacity_report(bloom):
    return {
        "bits": bloom.m,
        "hashes": bloom.k,
        "bytes": len(bloom.bits),
        "load": round(bloom.count / bloom.expected_items, 2),
    }


def screen(bloom, ids):
    maybe_seen = []
    new = []
    for scan_id in ids:
        (maybe_seen if bloom.contains(scan_id) else new).append(scan_id)
    return maybe_seen, new
