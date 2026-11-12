import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from broken import LatencyEWMA, RouteBoard, half_life_for_alpha


def test_first_sample_seeds_the_average():
    e = LatencyEWMA(half_life=10)
    assert e.update(200.0, ts=0) == 200.0, "with no history the best estimate is the sample itself"


def test_one_half_life_later_old_and_new_weigh_equally():
    e = LatencyEWMA(half_life=10)
    e.update(100.0, ts=0)
    assert e.update(200.0, ts=10) == pytest.approx(150.0)


def test_recent_samples_dominate_after_long_gap():
    e = LatencyEWMA(half_life=10)
    e.update(100.0, ts=0)
    value = e.update(300.0, ts=100)
    assert value == pytest.approx(300.0, abs=0.5), "after ten half-lives the old value is nearly forgotten"
    assert value > 200


def test_simultaneous_samples_do_not_move_the_average_much():
    e = LatencyEWMA(half_life=10)
    e.update(100.0, ts=5)
    assert e.update(500.0, ts=5) == pytest.approx(100.0), "dt of zero keeps all weight on history"


def test_out_of_order_timestamp_never_extrapolates():
    e = LatencyEWMA(half_life=10)
    e.update(100.0, ts=100)
    value = e.update(200.0, ts=90)
    assert 100.0 <= value <= 200.0, "a late-arriving sample must blend, not overshoot"
    assert e.last_ts == 100


def test_nan_and_negative_samples_are_rejected_and_counted():
    e = LatencyEWMA(half_life=10)
    e.update(100.0, ts=0)
    e.update(float("nan"), ts=1)
    e.update(float("inf"), ts=2)
    e.update(-5.0, ts=3)
    assert e.rejected == 3 and e.samples == 1
    assert e.value == pytest.approx(100.0) and not math.isnan(e.value)


def test_routes_are_tracked_independently_and_degradation_detected():
    board = RouteBoard(half_life=30, slow_factor=1.5)
    for i in range(30):
        board.record("/video", 100.0, i * 10)
        board.record("/images", 50.0, i * 10)
    assert not board.degraded("/video")
    for i in range(30, 36):
        board.record("/video", 400.0, i * 10)
        board.record("/images", 50.0, i * 10)
    assert board.degraded("/video")
    assert not board.degraded("/images")
    rows = {r["route"]: r for r in board.report()}
    assert rows["/images"]["ewma_ms"] == 50.0 and rows["/video"]["samples"] == 36


def test_half_life_matches_fixed_alpha():
    hl = half_life_for_alpha(0.5, interval=10)
    assert hl == pytest.approx(10.0)
    e = LatencyEWMA(half_life=hl)
    e.update(0.0, ts=0)
    assert e.update(100.0, ts=10) == pytest.approx(50.0)
