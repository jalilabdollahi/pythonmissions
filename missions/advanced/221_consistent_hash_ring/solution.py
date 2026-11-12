# Mission 221 - Tile Cache Hash Ring (solution)
# Consistent hash ring with virtual nodes for sharding tile caches.
import bisect
import hashlib


def _hash(key):
    return int(hashlib.md5(key.encode("utf-8")).hexdigest()[:8], 16)


class HashRing:
    def __init__(self, vnodes=50):
        self.vnodes = vnodes
        self._points = []
        self._owners = {}
        self._nodes = set()

    def _vnode_hashes(self, node):
        return [_hash(f"{node}#{i}") for i in range(self.vnodes)]

    def add_node(self, node):
        if node in self._nodes:
            return
        self._nodes.add(node)
        for h in self._vnode_hashes(node):
            if h in self._owners:
                continue
            self._owners[h] = node
            bisect.insort(self._points, h)

    def remove_node(self, node):
        if node not in self._nodes:
            return
        self._nodes.discard(node)
        for h in self._vnode_hashes(node):
            if self._owners.get(h) == node:
                del self._owners[h]
                self._points.remove(h)

    def _locate(self, key):
        idx = bisect.bisect_left(self._points, _hash(key))
        if idx == len(self._points):
            idx = 0
        return idx

    def get_node(self, key):
        if not self._points:
            return None
        return self._owners[self._points[self._locate(key)]]

    def get_nodes(self, key, count):
        if not self._points:
            return []
        want = min(count, len(self._nodes))
        start = self._locate(key)
        found = []
        for step in range(len(self._points)):
            point = self._points[(start + step) % len(self._points)]
            node = self._owners[point]
            if node not in found:
                found.append(node)
                if len(found) == want:
                    break
        return found

    def nodes(self):
        return sorted(self._nodes)


def routing_table(ring, keys):
    return {key: ring.get_node(key) for key in keys}
