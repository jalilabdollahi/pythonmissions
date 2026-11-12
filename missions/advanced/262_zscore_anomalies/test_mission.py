import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from broken import ZScoreDetector, group_incidents, scan

BASELINE = [10, 11, 9, 10, 10]


def feed(detector, values, start=0):
    return [detector.observe(start + i * 60, v) for i, v in enumerate(values)]


def test_warmup_never_alerts():
    det = ZScoreDetector(warmup=5)
    assert feed(det, [1, 100, 1, 100, 1]) == [None] * 5


def test_spike_is_judged_against_history_without_itself():
    det = ZScoreDetector(window=20, threshold=3.0)
    feed(det, BASELINE)
    hit = det.observe(999, 14)
    assert hit is not None, "a value must not be part of the baseline it is compared with"
    assert hit.z == pytest.approx(4 / math.sqrt(0.5))


def test_sample_standard_deviation_is_used():
    det = ZScoreDetector()
    feed(det, [2, 4, 4, 4, 5])
    # mean 3.8, sample variance 1.2
    assert det.zscore(5) == pytest.approx((5 - 3.8) / math.sqrt(1.2))


def test_drops_are_anomalies_too():
    det = ZScoreDetector()
    feed(det, BASELINE)
    hit = det.observe(500, 2)
    assert hit is not None and hit.z < 0, "traffic falling off a cliff is as bad as a spike"


def test_constant_baseline_flags_any_deviation_and_ignores_equal_values():
    det = ZScoreDetector()
    feed(det, [5, 5, 5, 5, 5])
    assert det.observe(1, 5) is None
    hit = det.observe(2, 6)
    assert hit is not None and math.isinf(hit.z) and hit.z > 0, "std 0 means any change is infinitely surprising"
    low = det.observe(3, 4)
    assert low is not None and low.z == -math.inf


def test_anomalies_do_not_poison_the_baseline():
    det = ZScoreDetector()
    feed(det, BASELINE)
    first = det.observe(1, 50)
    second = det.observe(2, 50)
    assert first is not None and second is not None, "an outage must keep alerting, not become normal"
    assert 50 not in det.values


def test_scan_finds_only_the_outage_minutes():
    series = [(i * 60, 10 + (i % 3)) for i in range(15)]
    series += [(900, 80), (960, 85), (1020, 11)]
    found = scan(series)
    assert [a.ts for a in found] == [900, 960]


def test_group_incidents_merges_nearby_hits():
    series = [(i * 60, 10 + (i % 2)) for i in range(12)]
    series += [(720, 70), (780, 90), (2000, 75)]
    incidents = group_incidents(scan(series), max_gap=120)
    assert [(i["start"], i["end"], i["count"], i["peak"]) for i in incidents] == [
        (720, 780, 2, 90),
        (2000, 2000, 1, 75),
    ]
