# Mission 223 - Flag Replica Causality
# Version-vector helpers for reconciling flag values across regional replicas.


def tick(clock, node):
    new = clock
    new[node] = new.get(node, 0) + 1
    return new


def merge(a, b):
    merged = {}
    for key in set(a):
        merged[key] = max(a.get(key, 0), b.get(key, 0))
    return merged


def compare(a, b):
    keys = set(a)
    a_le_b = all(a.get(k, 0) <= b.get(k, 0) for k in keys)
    b_le_a = all(b.get(k, 0) <= a.get(k, 0) for k in keys)
    if a_le_b and b_le_a:
        return "equal"
    if a_le_b:
        return "before"
    if b_le_a:
        return "after"
    return "concurrent"


def dominates(a, b):
    return compare(a, b) == "after"


def format_clock(clock):
    parts = [f"{node}:{count}" for node, count in sorted(clock.items()) if count]
    return "{" + ", ".join(parts) + "}"


def receive(local, remote, node):
    return merge(local, remote)


def resolve_siblings(versions):
    kept = []
    for version in versions:
        if any(compare(version, other) == "before" for other in versions):
            continue
        if any(compare(version, k) == "equal" for k in kept):
            continue
        kept.append(version)
    return kept


class Replica:
    def __init__(self, name):
        self.name = name
        self.clock = {}
        self.value = None

    def write(self, value):
        self.clock = tick(self.clock, self.name)
        self.value = value
        return self.clock

    def sync_from(self, other):
        relation = compare(self.clock, other.clock)
        if relation == "before":
            self.value = other.value
            self.clock = receive(self.clock, other.clock, self.name)
            return "fast-forward"
        if relation == "concurrent":
            return "conflict"
        return "noop"
