# Mission 230 - Top Talker Sketch
# Count-min sketch for approximate per-client request counts.
import hashlib
import math


class CountMinSketch:
    def __init__(self, epsilon=0.01, delta=0.01, width=None, depth=None):
        if width is None:
            width = math.ceil(1 / epsilon)
        if depth is None:
            depth = math.ceil(math.log(1 / delta))
        self.width = width
        self.depth = depth
        self.table = [[0] * width for _ in range(depth)]
        self.total = 0

    def _index(self, row, item):
        digest = hashlib.sha256(f"{item}".encode("utf-8")).digest()
        return int.from_bytes(digest[:8], "big") % self.width

    def update(self, item, count=1):
        if count < 0:
            raise ValueError("count-min sketches only support non-negative updates")
        for row in range(self.depth):
            self.table[row][self._index(row, item)] += count
        self.total += count

    def estimate(self, item):
        return max(self.table[row][self._index(row, item)] for row in range(self.depth))

    def merge(self, other):
        if (self.width, self.depth) != (other.width, other.depth):
            raise ValueError("sketches must have the same width and depth")
        for row in range(self.depth):
            for col in range(self.width):
                self.table[row][col] = max(self.table[row][col], other.table[row][col])
        self.total += other.total
        return self

    def update_many(self, items):
        for item in items:
            self.update(item)

    def fill_ratio(self):
        used = sum(1 for row in self.table for cell in row if cell)
        return used / (self.width * self.depth)

    def error_bound(self):
        return math.e / self.width * self.total


def build_from_log(lines, **shape):
    sketch = CountMinSketch(**shape)
    for line in lines:
        client = line.split()[0] if line.strip() else None
        if client:
            sketch.update(client)
    return sketch


def top_talkers(sketch, candidates, limit=3):
    scored = [(sketch.estimate(c), c) for c in candidates]
    scored.sort(key=lambda pair: (-pair[0], pair[1]))
    return [(name, count) for count, name in scored[:limit]]


def heavy_hitters(sketch, candidates, threshold_ratio):
    cutoff = sketch.total * threshold_ratio
    return sorted(c for c in candidates if sketch.estimate(c) >= cutoff)
