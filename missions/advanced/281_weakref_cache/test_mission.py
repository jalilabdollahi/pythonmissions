import gc
import os
import sys
import weakref

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import Texture, TextureCache, make_loader


def make_cache(**sizes):
    return TextureCache(make_loader(sizes))


def test_textures_support_weak_references():
    tex = Texture("sky", [1, 2])
    assert weakref.ref(tex)() is tex, "slotted classes need a __weakref__ slot"


def test_same_object_is_shared_while_in_use():
    cache = make_cache()
    first = cache.get("sky")
    assert cache.get("sky") is first
    assert cache.loads == 1 and cache.hits == 1


def test_unused_texture_is_freed():
    cache = make_cache()
    tex = cache.get("sky")
    assert cache.cached_names() == ["sky"]
    del tex
    gc.collect()
    assert cache.cached_names() == [], "nothing but the cache knows this texture, it must go"


def test_load_log_keeps_names_not_textures():
    cache = make_cache()
    tex = cache.get("sky")
    cache.get("rock")
    assert cache.load_log == ["sky", "rock"]
    del tex
    gc.collect()
    assert "sky" not in cache.cached_names(), "the audit log must not keep textures alive"


def test_empty_texture_is_still_a_hit():
    cache = make_cache(blank=0)
    blank = cache.get("blank")
    assert len(blank) == 0
    assert cache.get("blank") is blank
    assert cache.loads == 1, "an empty texture is falsy but alive; do not reload it"


def test_pinned_texture_survives_until_unpinned():
    cache = make_cache()
    cache.pin("sky")
    gc.collect()
    assert cache.cached_names() == ["sky"], "pinned textures are held strongly"
    assert cache.is_pinned("sky")
    cache.unpin("sky")
    gc.collect()
    assert cache.cached_names() == []
    assert cache.report()["pinned"] == 0


def test_hit_rate_counts_hits_over_requests():
    cache = make_cache()
    a = cache.get("a")
    cache.get("a")
    cache.get("a")
    cache.get("b")
    assert cache.hit_rate() == 0.5
    del a
