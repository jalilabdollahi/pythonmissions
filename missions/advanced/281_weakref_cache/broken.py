# Mission 281 - Texture Cache Leak
# Weak-value cache for render-farm textures that must not keep unused textures alive.
import weakref


class Texture:
    __slots__ = ("name", "pixels")

    def __init__(self, name, pixels):
        self.name = name
        self.pixels = pixels

    def __len__(self):
        return len(self.pixels)


class TextureCache:
    """Share loaded textures between render jobs without owning them."""

    def __init__(self, loader):
        self._loader = loader
        self._cache = weakref.WeakValueDictionary()
        self._pinned = {}
        self.loads = 0
        self.hits = 0
        self.load_log = []

    def get(self, name):
        tex = self._cache.get(name)
        if tex:
            self.hits += 1
            return tex
        tex = self._loader(name)
        self.loads += 1
        self.load_log.append(tex)
        self._cache[name] = tex
        return tex

    def pin(self, name):
        """Keep a hot texture alive even when no render job uses it."""
        self._pinned[name] = weakref.ref(self.get(name))

    def unpin(self, name):
        self._pinned.pop(name, None)

    def is_pinned(self, name):
        return name in self._pinned

    def cached_names(self):
        return sorted(self._cache.keys())

    def hit_rate(self):
        total = self.hits + self.loads
        return self.hits / total if total else 0.0

    def report(self):
        return {
            "cached": len(self._cache),
            "pinned": len(self._pinned),
            "loads": self.loads,
            "hits": self.hits,
        }


def make_loader(sizes):
    """Build a loader that fabricates textures with the given pixel counts."""

    def load(name):
        return Texture(name, [0] * sizes.get(name, 4))

    return load


if __name__ == "__main__":
    cache = TextureCache(make_loader({"sky": 8}))
    sky = cache.get("sky")
    print(cache.report(), len(sky))
