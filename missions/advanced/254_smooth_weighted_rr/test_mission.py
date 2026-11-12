import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from broken import NoBackendAvailable, SmoothBalancer


def longest_run(seq, name):
    best = run = 0
    for item in seq:
        run = run + 1 if item == name else 0
        best = max(best, run)
    return best


def test_classic_nginx_sequence_for_5_1_1():
    lb = SmoothBalancer({"a": 5, "b": 1, "c": 1})
    assert lb.sequence(7) == ["a", "a", "b", "a", "c", "a", "a"]


def test_heavy_backend_is_interleaved_not_bursty():
    lb = SmoothBalancer({"a": 5, "b": 1, "c": 1})
    seq = lb.sequence(70)
    assert seq.count("a") == 50 and seq.count("b") == 10 and seq.count("c") == 10
    assert longest_run(seq, "a") <= 4, "smooth round-robin interleaves; plain weighted round-robin would send 5 in a row"


def test_equal_weights_are_plain_round_robin_in_config_order():
    lb = SmoothBalancer({"a": 1, "b": 1, "c": 1})
    assert lb.sequence(6) == ["a", "b", "c", "a", "b", "c"], "ties go to the first backend in config order"


def test_down_backend_is_skipped_and_shares_use_remaining_total():
    lb = SmoothBalancer({"a": 5, "b": 1, "c": 1})
    lb.mark_down("c")
    seq = lb.sequence(12)
    assert "c" not in seq
    assert seq.count("a") == 10 and seq.count("b") == 2, "weights are shared out among the backends that are up"


def test_recovered_backend_starts_with_a_clean_slate():
    lb = SmoothBalancer({"a": 3, "b": 1})
    assert lb.pick() == "a"  # a now holds -1 credit
    lb.mark_down("a")
    lb.mark_up("a")
    assert lb._find("a").current == 0, "stale credit from before the outage must be discarded"
    lb.mark_down("b")
    lb.mark_up("b")
    assert lb.sequence(4) == ["a", "a", "b", "a"], "after recovery the cycle restarts from the beginning"


def test_set_weight_changes_future_shares():
    lb = SmoothBalancer({"a": 1, "b": 1})
    lb.set_weight("b", 3)
    seq = lb.sequence(8)
    assert seq.count("a") == 2 and seq.count("b") == 6
    assert lb.shares() == {"a": 0.25, "b": 0.75}


def test_no_backend_available_and_zero_weight_is_never_picked():
    lb = SmoothBalancer({"a": 0, "b": 2})
    assert set(lb.sequence(5)) == {"b"}
    lb.mark_down("b")
    with pytest.raises(NoBackendAvailable):
        lb.pick()
    with pytest.raises(ValueError):
        SmoothBalancer({"x": -1})


def test_add_and_remove_backends():
    lb = SmoothBalancer({"a": 1})
    lb.add("b", 1)
    assert lb.sequence(4) == ["a", "b", "a", "b"]
    lb.remove("a")
    assert lb.sequence(2) == ["b", "b"]
