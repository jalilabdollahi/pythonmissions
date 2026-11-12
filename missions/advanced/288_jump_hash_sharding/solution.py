# Mission 288 - Shard Router (solution)
# Jump consistent hashing to route keys to shards with minimal movement on resize.
import hashlib

MASK = 0xFFFFFFFFFFFFFFFF
MULTIPLIER = 2862933555777941757


def key_to_int(key):
    """Spread a string key over 64 bits."""
    return int.from_bytes(hashlib.sha256(key.encode("utf-8")).digest()[:8], "big")


def jump_hash(key, buckets):
    """Lamping & Veach jump consistent hash: bucket index in [0, buckets)."""
    if buckets <= 0:
        raise ValueError("need at least one bucket")
    b, j = -1, 0
    while j < buckets:
        b = j
        key = (key * MULTIPLIER + 1) & MASK
        j = int((b + 1) * (float(1 << 31) / float((key >> 33) + 1)))
    return b


def route(key, shards):
    """Pick a shard name. The shard list is append-only: new shards go on the end."""
    return shards[jump_hash(key_to_int(key), len(shards))]


def distribution(keys, shards):
    counts = {name: 0 for name in shards}
    for key in keys:
        counts[route(key, shards)] += 1
    return counts


def moved_keys(keys, old_shards, new_shards):
    """Keys whose owning shard changes when the shard list changes."""
    return [k for k in keys if route(k, old_shards) != route(k, new_shards)]


def plan_resize(keys, old_shards, new_shards):
    moved = moved_keys(keys, old_shards, new_shards)
    targets = {}
    for key in moved:
        targets.setdefault(route(key, new_shards), []).append(key)
    return {
        "moved": len(moved),
        "fraction": len(moved) / len(keys) if keys else 0.0,
        "targets": {shard: len(items) for shard, items in sorted(targets.items())},
    }


class ShardRouter:
    """Owns the append-only shard list so nobody reorders it by accident."""

    def __init__(self, shards):
        self._shards = list(shards)

    @property
    def shards(self):
        return tuple(self._shards)

    def route(self, key):
        return route(key, self._shards)

    def add_shard(self, name, keys=()):
        """Append a shard and report how many of `keys` would move onto it."""
        if name in self._shards:
            raise ValueError(f"shard {name!r} already exists")
        before = list(self._shards)
        self._shards.append(name)
        return plan_resize(list(keys), before, self._shards)
