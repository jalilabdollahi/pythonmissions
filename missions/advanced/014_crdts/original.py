# Mission 014 (Advanced) - CRDT G-Counter
# Fix the 2 bugs in this script.

class GCounter:
    def __init__(self, node_id):
        self.node_id = node_id
        self._counts = {node_id: 0}

    def increment(self, amount=1):
        self._counts[self.node_id] += amount

    def value(self):
        return max(self._counts.values())  # BUG 1: should be sum, not max

    def merge(self, other):
        """Merge another GCounter into this one."""
        result_counts = dict(self._counts)
        for node, count in other._counts.items():
            result_counts[node] = result_counts.get(node, 0) + count  # BUG 2: should take max, not add
        return GCounter._from_counts(self.node_id, result_counts)

    @classmethod
    def _from_counts(cls, node_id, counts):
        g = cls(node_id)
        g._counts = counts
        return g

    def __repr__(self):
        return f"GCounter({self.node_id}, value={self.value()})"
