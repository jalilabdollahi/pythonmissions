import copy
import os
import sys
from datetime import datetime

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def w(start, end, team):
    return {"start": f"2025-03-01 {start}", "end": f"2025-03-01 {end}", "team": team}


def test_disjoint_windows_stay_separate():
    out = broken.merge_windows([w("01:00", "02:00", "db"), w("04:00", "05:00", "net")])
    assert [(m["start"][-5:], m["end"][-5:]) for m in out] == [("01:00", "02:00"), ("04:00", "05:00")]


def test_overlapping_windows_merge_and_collect_teams():
    out = broken.merge_windows([w("01:00", "03:00", "db"), w("02:00", "04:00", "net")])
    assert len(out) == 1
    assert out[0]["start"].endswith("01:00") and out[0]["end"].endswith("04:00")
    assert out[0]["teams"] == ["db", "net"]


def test_touching_windows_are_one_window():
    out = broken.merge_windows([w("01:00", "02:00", "db"), w("02:00", "03:00", "net")])
    assert len(out) == 1, "back-to-back windows are one continuous outage"
    assert out[0]["end"].endswith("03:00")


def test_contained_window_does_not_shorten_the_merge():
    out = broken.merge_windows([w("01:00", "06:00", "db"), w("02:00", "03:00", "net")])
    assert len(out) == 1
    assert out[0]["end"].endswith("06:00"), "the merged end is the later of the two ends"


def test_input_order_does_not_matter():
    shuffled = [w("04:00", "05:00", "c"), w("01:00", "02:30", "a"), w("02:00", "04:00", "b")]
    out = broken.merge_windows(shuffled)
    assert len(out) == 1
    assert out[0]["start"].endswith("01:00") and out[0]["end"].endswith("05:00")
    assert out[0]["teams"] == ["a", "b", "c"]


def test_input_is_not_modified_and_result_sorted():
    data = [w("08:00", "09:00", "x"), w("01:00", "02:00", "y")]
    snapshot = copy.deepcopy(data)
    out = broken.merge_windows(data)
    assert data == snapshot
    assert out[0]["start"] < out[1]["start"]


def test_invalid_window_rejected():
    with pytest.raises(ValueError):
        broken.merge_windows([w("05:00", "05:00", "x")])


def test_in_window_start_inclusive_end_exclusive():
    merged = broken.merge_windows([w("01:00", "02:00", "db")])
    assert broken.in_window(merged, datetime(2025, 3, 1, 1, 0))
    assert broken.in_window(merged, datetime(2025, 3, 1, 1, 59))
    assert not broken.in_window(merged, datetime(2025, 3, 1, 2, 0))
