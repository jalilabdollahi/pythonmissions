import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken

EVENTS = [
    {"service": "api", "ms": 30},
    {"service": "db", "ms": 40},
    {"service": "api", "ms": 50},
    {"service": "cache", "ms": 2},
    {"service": "db", "ms": 90},
]


def test_each_service_appears_once():
    totals = broken.per_service_totals(EVENTS)
    assert sorted(totals) == ["api", "cache", "db"]


def test_counts_and_totals_cover_all_events_of_a_service():
    totals = broken.per_service_totals(EVENTS)
    assert totals["api"] == {"count": 2, "total_ms": 80}, "groupby needs data sorted by the grouping key"
    assert totals["db"] == {"count": 2, "total_ms": 130}
    assert totals["cache"] == {"count": 1, "total_ms": 2}


def test_input_order_does_not_matter():
    shuffled = list(reversed(EVENTS))
    assert broken.per_service_totals(shuffled) == broken.per_service_totals(EVENTS)


def test_group_data_is_not_lost_when_groupby_advances():
    events = [{"service": "a", "ms": 1}, {"service": "b", "ms": 2}, {"service": "c", "ms": 3}]
    totals = broken.per_service_totals(events)
    assert totals["a"]["total_ms"] == 1 and totals["b"]["total_ms"] == 2


def test_empty_events():
    assert broken.per_service_totals([]) == {}


def test_longest_failing_streak_uses_original_order():
    assert broken.longest_failing_streak([False, False, True, False]) == 2, "do not sort a time series"


def test_streak_edge_cases():
    assert broken.longest_failing_streak([]) == 0
    assert broken.longest_failing_streak([True, True]) == 0
    assert broken.longest_failing_streak([False, True, False, False, False, True]) == 3
