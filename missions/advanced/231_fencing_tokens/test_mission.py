import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import FencedStore, LockService, StaleTokenError, run_job


class Clock:
    def __init__(self):
        self.now = 1000.0

    def __call__(self):
        return self.now


def make(lease=10.0):
    clock = Clock()
    return LockService(clock, lease), FencedStore(), clock


def test_first_grant_gets_token_one_and_blocks_others():
    svc, _, _ = make()
    assert svc.acquire("A") == 1
    assert svc.acquire("B") is None, "live lease must refuse other clients"


def test_holder_reacquire_keeps_its_token_and_extends_lease():
    svc, _, clock = make(10)
    assert svc.acquire("A") == 1
    clock.now += 6
    assert svc.acquire("A") == 1
    clock.now += 6
    assert svc.acquire("B") is None, "renewal at +6 pushed expiry to +16"


def test_lease_ends_exactly_at_expiry_instant():
    svc, _, clock = make(10)
    svc.acquire("A")
    clock.now += 9.99
    assert svc.acquire("B") is None
    clock.now += 0.01
    assert svc.acquire("B") == 2, "now == expires_at means the lease is over"


def test_takeover_after_expiry_mints_a_new_token():
    svc, _, clock = make(10)
    first = svc.acquire("A")
    clock.now += 30
    second = svc.acquire("B")
    assert second > first, "a takeover without release must still increase the token"


def test_zombie_writer_is_rejected_by_the_store():
    svc, store, clock = make(10)
    a_token = svc.acquire("A")
    store.write("manifest", "a-v1", a_token)
    clock.now += 60
    b_token = svc.acquire("B")
    store.write("manifest", "b-v1", b_token)
    with pytest.raises(StaleTokenError):
        store.write("manifest", "a-zombie", a_token)
    assert store.read("manifest") == "b-v1"


def test_live_holder_can_write_repeatedly_with_same_token():
    svc, store, _ = make()
    token = svc.acquire("A")
    store.write("k", 1, token)
    store.write("k", 2, token)
    assert store.read("k") == 2


def test_high_water_mark_never_goes_down():
    store = FencedStore()
    store.write("k", "new", 5)
    with pytest.raises(StaleTokenError):
        store.write("k", "older", 3)
    with pytest.raises(StaleTokenError):
        store.write("k", "older-still", 4)
    assert store.highest_token == 5
    assert store.writers_seen() == [5], "rejected writes must leave no trace"


def test_stale_release_does_not_free_the_new_holders_lock():
    svc, _, clock = make(10)
    a = svc.acquire("A")
    clock.now += 20
    b = svc.acquire("B")
    assert svc.release("A", a) is False
    assert svc.current_token() == b
    assert run_job(svc, FencedStore(), "C", "k", "v") == "busy"
