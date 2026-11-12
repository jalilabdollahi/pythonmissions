import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import CountMinSketch, build_from_log, heavy_hitters, top_talkers


def test_shape_follows_epsilon_and_delta():
    s = CountMinSketch(epsilon=0.01, delta=0.01)
    assert s.width == 272, "width = ceil(e / epsilon)"
    assert s.depth == 5, "depth = ceil(ln(1 / delta))"
    assert len(s.table) == 5 and len(s.table[0]) == 272


def test_never_undercounts_and_is_exact_without_collisions():
    s = CountMinSketch(epsilon=0.001, delta=0.001)
    s.update("10.0.0.1", 7)
    s.update("10.0.0.1")
    s.update("10.0.0.2", 3)
    assert s.estimate("10.0.0.1") == 8
    assert s.estimate("10.0.0.2") == 3
    assert s.estimate("10.9.9.9") == 0


def test_negative_updates_are_rejected():
    with pytest.raises(ValueError):
        CountMinSketch().update("a", -1)


def test_estimate_is_the_minimum_over_rows_not_the_worst_collision():
    s = CountMinSketch(width=4, depth=6)
    s.update("heavy", 1000)
    s.update("light", 1)
    assert s.estimate("light") < 1000, "min over rows discards the rows where light collides with heavy"


def test_rows_use_independent_hashes():
    s = CountMinSketch(width=8, depth=4)
    s.update("heavy", 1000)
    full_collisions = sum(1 for i in range(300) if s.estimate(f"unseen-{i}") >= 1000)
    assert full_collisions < 10, "an item colliding in ALL rows means the rows are not independent"


def test_merge_adds_counts_from_both_routers():
    a, b = CountMinSketch(width=64, depth=4), CountMinSketch(width=64, depth=4)
    a.update("client", 5)
    b.update("client", 7)
    b.update("only-b", 2)
    a.merge(b)
    assert a.estimate("client") == 12
    assert a.estimate("only-b") >= 2
    assert a.total == 14


def test_merge_requires_identical_shape():
    with pytest.raises(ValueError):
        CountMinSketch(width=10, depth=3).merge(CountMinSketch(width=11, depth=3))


def test_build_from_log_skips_blank_lines():
    log = ["10.0.0.1 GET /", "", "10.0.0.2 GET /x", "10.0.0.1 POST /y", "   "]
    s = build_from_log(log, width=128, depth=4)
    assert s.total == 3 and s.estimate("10.0.0.1") == 2
    assert 0 < s.fill_ratio() <= 1
    assert s.error_bound() == pytest.approx(2.718281828 / 128 * 3)


def test_top_talkers_and_heavy_hitters():
    s = CountMinSketch(epsilon=0.001, delta=0.001)
    for name, n in (("a", 50), ("b", 30), ("c", 5), ("d", 1)):
        s.update(name, n)
    assert top_talkers(s, ["a", "b", "c", "d"], limit=2) == [("a", 50), ("b", 30)]
    assert heavy_hitters(s, ["a", "b", "c", "d"], 0.1) == ["a", "b"]
