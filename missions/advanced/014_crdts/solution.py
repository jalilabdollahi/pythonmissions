# Mission 014 (Advanced) - CRDT G-Counter
# Fixed solution

class GCounter:
    def __init__(self, node_id):
        self.node_id = node_id
        self._counts = {node_id: 0}

    def increment(self, amount=1):
        self._counts[self.node_id] += amount

    def value(self):
        return sum(self._counts.values())

    def merge(self, other):
        result_counts = dict(self._counts)
        for node, count in other._counts.items():
            result_counts[node] = max(result_counts.get(node, 0), count)
        return GCounter._from_counts(self.node_id, result_counts)

    @classmethod
    def _from_counts(cls, node_id, counts):
        g = cls(node_id)
        g._counts = counts
        return g

    def __repr__(self):
        return f"GCounter({self.node_id}, value={self.value()})"
