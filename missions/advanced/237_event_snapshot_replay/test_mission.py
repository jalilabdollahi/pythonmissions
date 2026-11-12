import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import PoolStore, apply_event, empty_pool, free_seats, rehydrate, should_snapshot, take_snapshot


def ev(version, kind, **data):
    return {"version": version, "type": kind, "data": data}


STREAM = [
    ev(1, "seats_added", count=5),
    ev(2, "seat_assigned", user="ana"),
    ev(3, "seat_assigned", user="bo"),
    ev(4, "seat_revoked", user="ana"),
    ev(5, "seats_added", count=2),
]


def test_full_replay_without_snapshot():
    state, version = rehydrate(None, STREAM)
    assert state == {"seats": 7, "assigned": {"bo"}} and version == 5
    assert free_seats(state) == 6


def test_snapshot_then_newer_events_equals_full_replay():
    upto3 = rehydrate(None, STREAM[:3])[0]
    snap = take_snapshot(upto3, 3)
    assert rehydrate(snap, STREAM) == rehydrate(None, STREAM)


def test_event_at_snapshot_version_is_not_replayed_again():
    snap = take_snapshot({"seats": 5, "assigned": set()}, 1)
    state, version = rehydrate(snap, STREAM[:1])
    assert state["seats"] == 5, "version 1 is already inside the snapshot"
    assert version == 1


def test_snapshot_is_independent_of_the_live_state():
    live = {"seats": 3, "assigned": {"ana"}}
    snap = take_snapshot(live, 10)
    apply_event(live, ev(11, "seat_assigned", user="bo"))
    assert snap["state"]["assigned"] == {"ana"}, "snapshots are history, later events must not leak in"


def test_rehydrate_does_not_mutate_the_snapshot():
    snap = take_snapshot({"seats": 1, "assigned": set()}, 1)
    rehydrate(snap, [ev(2, "seat_assigned", user="ana")])
    assert snap["state"]["assigned"] == set()


def test_events_are_applied_in_version_order_even_if_loaded_shuffled():
    shuffled = [STREAM[3], STREAM[1], STREAM[0], STREAM[2], STREAM[4]]
    state, version = rehydrate(None, shuffled)
    assert state["assigned"] == {"bo"}, "revoke at v4 must come after assign at v2"
    assert version == 5


def test_gap_in_versions_is_an_error():
    snap = take_snapshot({"seats": 5, "assigned": set()}, 1)
    with pytest.raises(ValueError):
        rehydrate(snap, [ev(2, "seat_assigned", user="a"), ev(4, "seat_assigned", user="b")])


def test_store_checkpoint_and_snapshot_policy():
    store = PoolStore()
    store.append("seats_added", count=3)
    store.append("seat_assigned", user="ana")
    assert store.checkpoint() == 2
    store.append("seat_assigned", user="bo")
    assert store.load() == ({"seats": 3, "assigned": {"ana", "bo"}}, 3)
    assert should_snapshot(150, 50) and not should_snapshot(149, 50)
    with pytest.raises(ValueError):
        apply_event(empty_pool(), ev(1, "bogus"))
