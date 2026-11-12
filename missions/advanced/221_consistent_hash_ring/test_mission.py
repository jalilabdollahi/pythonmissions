import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken
from broken import HashRing, routing_table

LAYOUT = {"A#0": 100, "A#1": 150, "B#0": 200, "B#1": 400}


def fake_ring(monkeypatch, key_hashes):
    table = dict(LAYOUT)
    table.update(key_hashes)
    monkeypatch.setattr(broken, "_hash", lambda s: table[s])
    ring = HashRing(vnodes=2)
    ring.add_node("A")
    ring.add_node("B")
    return ring


def test_key_owned_by_next_point_clockwise(monkeypatch):
    ring = fake_ring(monkeypatch, {"k": 160})
    assert ring.get_node("k") == "B", "hash 160 -> first point >= 160 is B#0 at 200"


def test_hash_equal_to_point_belongs_to_that_point(monkeypatch):
    ring = fake_ring(monkeypatch, {"k": 150})
    assert ring.get_node("k") == "A", "a hash equal to a point is owned by that point"


def test_lookup_wraps_past_the_last_point(monkeypatch):
    ring = fake_ring(monkeypatch, {"k": 450})
    assert ring.get_node("k") == "A", "past 400 the ring wraps to the first point (A#0)"


def test_removed_node_owns_nothing(monkeypatch):
    ring = fake_ring(monkeypatch, {"k1": 160, "k2": 399, "k3": 50})
    ring.remove_node("B")
    assert ring.nodes() == ["A"]
    assert [ring.get_node(k) for k in ("k1", "k2", "k3")] == ["A", "A", "A"]


def test_replicas_are_distinct_physical_nodes(monkeypatch):
    ring = fake_ring(monkeypatch, {"k": 90})
    assert ring.get_nodes("k", 2) == ["A", "B"], "A#0 and A#1 are the same host"
    assert ring.get_nodes("k", 5) == ["A", "B"], "cannot return more nodes than exist"


def test_empty_ring_returns_nothing():
    ring = HashRing()
    assert ring.get_node("x") is None
    assert ring.get_nodes("x", 2) == []


def test_removal_only_moves_keys_of_removed_node():
    ring = HashRing(vnodes=100)
    for n in ("tile-01", "tile-02", "tile-03", "tile-04"):
        ring.add_node(n)
    keys = [f"z{i}/x{i * 7}" for i in range(2000)]
    before = routing_table(ring, keys)
    ring.remove_node("tile-03")
    after = routing_table(ring, keys)
    for k in keys:
        if before[k] != "tile-03":
            assert after[k] == before[k], "keys on surviving nodes must not move"
        else:
            assert after[k] != "tile-03"
