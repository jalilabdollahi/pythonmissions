import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def test_oldest_entry_is_evicted_first():
    cache = broken.LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)
    assert cache.keys() == ["b", "c"], "a was least recently used and must be evicted"


def test_newest_entry_survives_eviction():
    cache = broken.LRUCache(1)
    cache.put("old", 1)
    cache.put("new", 2)
    assert "new" in cache and "old" not in cache


def test_get_refreshes_recency():
    cache = broken.LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    assert cache.get("a") == 1
    cache.put("c", 3)
    assert cache.keys() == ["a", "c"], "reading a made b the least recently used"


def test_overwrite_refreshes_recency():
    cache = broken.LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("a", 10)
    cache.put("c", 3)
    assert cache.keys() == ["a", "c"]
    assert cache.get("a") == 10


def test_missing_key_returns_none_without_side_effects():
    cache = broken.LRUCache(2)
    cache.put("a", 1)
    assert cache.get("zzz") is None
    assert cache.keys() == ["a"]


def test_eviction_counter_and_len():
    cache = broken.LRUCache(2)
    for i in range(5):
        cache.put(i, i)
    assert len(cache) == 2
    assert cache.evictions == 3


def test_capacity_must_be_positive():
    with pytest.raises(ValueError):
        broken.LRUCache(0)
