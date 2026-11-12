# Mission 227 - Shared Watchlist Merge (solution)
# Observed-remove set (OR-Set) for a watchlist edited on several replicas.


class ORSet:
    def __init__(self, replica):
        self.replica = replica
        self._seq = 0
        self.adds = {}
        self.tombstones = set()

    def _new_tag(self):
        self._seq += 1
        return (self.replica, self._seq)

    def add(self, element):
        tag = self._new_tag()
        self.adds.setdefault(element, set()).add(tag)
        return tag

    def remove(self, element):
        observed = self.adds.get(element)
        if not observed:
            return False
        self.tombstones.update(observed)
        return True

    def contains(self, element):
        live = self.adds.get(element, set()) - self.tombstones
        return bool(live)

    def elements(self):
        return sorted(e for e in self.adds if self.contains(e))

    def merge(self, other):
        for element, tags in other.adds.items():
            self.adds.setdefault(element, set()).update(tags)
        self.tombstones |= other.tombstones
        return self

    def compact(self):
        for element in list(self.adds):
            self.adds[element] -= self.tombstones
            if not self.adds[element]:
                del self.adds[element]
        live = set()
        for tags in self.adds.values():
            live |= tags
        self.tombstones &= live
        return self

    def state_size(self):
        return sum(len(t) for t in self.adds.values()) + len(self.tombstones)


def snapshot(orset):
    return {
        "replica": orset.replica,
        "elements": orset.elements(),
        "tags": orset.state_size(),
    }


def merge_all(replica_name, *others):
    merged = ORSet(replica_name)
    for other in others:
        merged.merge(other)
    return merged


def sync(a, b):
    a_before, b_before = a.elements(), b.elements()
    a.merge(b)
    b.merge(a)
    return a_before != a.elements() or b_before != b.elements()
