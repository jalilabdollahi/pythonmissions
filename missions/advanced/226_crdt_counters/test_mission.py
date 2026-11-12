import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import GCounter, PNCounter, contributors, converge, describe


def test_gcounter_value_is_sum_of_slots():
    c = GCounter()
    c.increment("sfo", 3)
    c.increment("ams", 4)
    c.increment("sfo")
    assert c.value() == 8


def test_gcounter_rejects_zero_and_negative_amounts():
    c = GCounter()
    for bad in (0, -1):
        with pytest.raises(ValueError):
            c.increment("sfo", bad)


def test_merge_keeps_the_larger_slot_even_when_remote_is_behind():
    local = GCounter({"sfo": 10})
    stale = GCounter({"sfo": 4, "ams": 2})
    local.merge(stale)
    assert local.to_dict() == {"ams": 2, "sfo": 10}, "a counter slot can never go backwards"


def test_merge_is_idempotent():
    a = GCounter({"sfo": 5})
    b = GCounter({"ams": 3, "sfo": 5})
    a.merge(b)
    first = a.value()
    a.merge(b)
    a.merge(b.copy())
    assert a.value() == first == 8, "re-delivered state must not be double counted"


def test_merge_is_commutative():
    a = GCounter({"x": 1, "y": 7})
    b = GCounter({"x": 4, "z": 2})
    assert a.copy().merge(b).to_dict() == b.copy().merge(a).to_dict()


def test_pncounter_propagates_decrements_through_merge():
    left, right = PNCounter(), PNCounter()
    left.increment("sfo", 10)
    right.decrement("ams", 4)
    left.merge(right)
    assert left.value() == 6, "decrements recorded elsewhere must reach us"
    right.merge(left)
    assert right.value() == 6


def test_pncounter_value_may_be_negative():
    c = PNCounter()
    c.increment("sfo", 2)
    c.decrement("ams", 5)
    assert c.value() == -3, "do not clamp: clamping makes replicas disagree after merging"


def test_replicas_converge_after_full_gossip():
    a, b, c = PNCounter(), PNCounter(), PNCounter()
    a.increment("a", 5)
    b.decrement("b", 2)
    c.increment("c", 1)
    c.decrement("c", 4)
    assert converge([a, b, c]) == -0 + 5 - 2 + 1 - 4
    assert contributors(a) == ["a", "b", "c"]
    assert describe(a) == "PN(+6 -6 = 0)"
    assert describe(GCounter({"x": 2})) == "G(2)"
