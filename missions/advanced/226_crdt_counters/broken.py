# Mission 226 - Edge Counter Convergence
# State-based CRDT counters (G-Counter and PN-Counter) for edge POP metrics.


class GCounter:
    def __init__(self, counts=None):
        self.counts = dict(counts or {})

    def increment(self, node, amount=1):
        if amount < 0:
            raise ValueError("a grow-only counter only accepts positive amounts")
        self.counts[node] = self.counts.get(node, 0) + amount

    def value(self):
        return sum(self.counts.values())

    def merge(self, other):
        for node, count in other.counts.items():
            self.counts[node] = count
        return self

    def copy(self):
        return GCounter(self.counts)

    def to_dict(self):
        return dict(sorted(self.counts.items()))


class PNCounter:
    def __init__(self):
        self.pos = GCounter()
        self.neg = GCounter()

    def increment(self, node, amount=1):
        self.pos.increment(node, amount)

    def decrement(self, node, amount=1):
        self.neg.increment(node, amount)

    def value(self):
        return max(0, self.pos.value() - self.neg.value())

    def merge(self, other):
        self.pos.merge(other.pos)
        return self

    def copy(self):
        clone = PNCounter()
        clone.pos = self.pos.copy()
        clone.neg = self.neg.copy()
        return clone


def converge(replicas):
    """Gossip every replica into every other until all agree; returns the value."""
    snapshots = [r.copy() for r in replicas]
    for replica in replicas:
        for snap in snapshots:
            replica.merge(snap)
    values = {r.value() for r in replicas}
    if len(values) != 1:
        raise RuntimeError(f"replicas diverged: {sorted(values)}")
    return values.pop()


def contributors(counter):
    if isinstance(counter, PNCounter):
        return sorted(set(counter.pos.counts) | set(counter.neg.counts))
    return sorted(counter.counts)


def describe(counter):
    if isinstance(counter, PNCounter):
        return f"PN(+{counter.pos.value()} -{counter.neg.value()} = {counter.value()})"
    return f"G({counter.value()})"
