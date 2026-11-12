import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import SequenceTracker, deliver, lossy_producers


def test_in_order_stream_is_all_ok():
    tracker = SequenceTracker()
    assert [tracker.accept("t1", n) for n in (1, 2, 3)] == ["ok", "ok", "ok"]
    assert tracker.is_complete("t1")


def test_skipped_numbers_are_all_reported_as_gaps():
    tracker = SequenceTracker()
    tracker.accept("t1", 1)
    assert tracker.accept("t1", 5) == "gap"
    assert tracker.gaps("t1") == [2, 3, 4], "every skipped number is missing, including seq-1"
    assert not tracker.is_complete("t1")


def test_resent_message_is_a_duplicate_even_when_it_is_the_latest():
    tracker = SequenceTracker()
    assert tracker.accept("t1", 1) == "ok"
    assert tracker.accept("t1", 1) == "duplicate"
    assert tracker.accept("t1", 2) == "ok"
    assert tracker.accept("t1", 2) == "duplicate"


def test_late_arrival_fills_the_gap_exactly_once():
    tracker = SequenceTracker()
    for seq in (1, 4):
        tracker.accept("t1", seq)
    assert tracker.accept("t1", 2) == "late"
    assert tracker.gaps("t1") == [3]
    assert tracker.accept("t1", 2) == "duplicate", "a filled gap must not be filled twice"
    assert tracker.accept("t1", 3) == "late"
    assert tracker.is_complete("t1")


def test_producers_do_not_share_gaps():
    tracker = SequenceTracker()
    tracker.accept("turbine-a", 1)
    tracker.accept("turbine-a", 4)
    tracker.accept("turbine-b", 1)
    assert tracker.gaps("turbine-b") == [], "turbine-b lost nothing"
    assert tracker.gaps("turbine-a") == [2, 3]


def test_deliver_drops_only_duplicates():
    tracker = SequenceTracker()
    messages = [("a", 1, "r1"), ("a", 3, "r3"), ("a", 1, "r1-again"), ("a", 2, "r2"), ("a", 3, "r3-again")]
    assert deliver(tracker, messages) == ["r1", "r3", "r2"]
    assert tracker.counts == {"ok": 1, "gap": 1, "late": 1, "duplicate": 2}


def test_unknown_producer_has_no_history():
    tracker = SequenceTracker()
    assert tracker.gaps("ghost") == []
    assert tracker.highest("ghost") == 0
    assert not tracker.is_complete("ghost")


def test_gap_ranges_collapse_consecutive_numbers():
    tracker = SequenceTracker()
    for seq in (1, 4, 5, 9):
        tracker.accept("t1", seq)
    tracker.accept("t2", 1)
    assert tracker.gap_ranges("t1") == [(2, 3), (6, 8)]
    assert lossy_producers(tracker) == {"t1": [(2, 3), (6, 8)]}
