import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


class Clock:
    def __init__(self):
        self.now = 0

    def __call__(self):
        return self.now


def make(ttl=10):
    clock = Clock()
    return broken.TTLCache(ttl, clock), clock


def test_value_is_returned_while_fresh():
    cache, clock = make()
    cache.set("quote-api", "10.0.0.5")
    clock.now = 9
    assert cache.get("quote-api") == "10.0.0.5"


def test_entry_expires_exactly_at_ttl():
    cache, clock = make()
    cache.set("k", "v")
    clock.now = 10
    assert cache.get("k") is None, "age == ttl is already expired"


def test_expired_entry_returns_default():
    cache, clock = make()
    cache.set("k", "v")
    clock.now = 11
    assert cache.get("k", "gone") == "gone"


def test_overwrite_restarts_the_lifetime():
    cache, clock = make()
    cache.set("k", "old")
    clock.now = 8
    cache.set("k", "new")
    clock.now = 15
    assert cache.get("k") == "new", "set() must store a fresh timestamp"


def test_size_ignores_expired_entries():
    cache, clock = make()
    cache.set("a", 1)
    clock.now = 5
    cache.set("b", 2)
    clock.now = 12
    assert cache.size() == 1, "only b is still alive"


def test_purge_reports_removed_count():
    cache, clock = make(ttl=5)
    for key in "abc":
        cache.set(key, 1)
    clock.now = 5
    assert cache.purge() == 3


def test_get_or_load_reloads_after_expiry():
    cache, clock = make()
    calls = []

    def loader():
        calls.append(clock.now)
        return f"v{len(calls)}"

    assert cache.get_or_load("k", loader) == "v1"
    clock.now = 3
    assert cache.get_or_load("k", loader) == "v1"
    clock.now = 10
    assert cache.get_or_load("k", loader) == "v2"
    assert calls == [0, 10]
