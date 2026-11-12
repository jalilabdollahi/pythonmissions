import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from broken import correlate, failing_requests, hops, slowest_gap, summarize


def line(ts, service, seq, rid, msg="m", level="INFO"):
    return {"ts": ts, "service": service, "seq": seq, "request_id": rid, "msg": msg, "level": level}


def test_ids_differing_in_case_or_whitespace_are_one_request():
    entries = [line(1.0, "edge", 1, "REQ-9"), line(2.0, "router", 1, " req-9 "), line(3.0, "billing", 1, "req-9")]
    timelines, unattributed = correlate(entries)
    assert list(timelines) == ["req-9"]
    assert len(timelines["req-9"]) == 3 and unattributed == 0


def test_lines_without_an_id_are_counted_not_grouped():
    entries = [line(1.0, "edge", 1, None), line(2.0, "edge", 2, "  "), line(3.0, "edge", 3, "a")]
    timelines, unattributed = correlate(entries)
    assert unattributed == 2 and list(timelines) == ["a"]


def test_clock_skew_is_subtracted_for_services_running_ahead():
    entries = [
        line(100.0, "edge", 1, "a"),
        line(105.5, "warehouse", 1, "a"),  # warehouse clock runs 5s ahead: true time 100.5
    ]
    timelines, _ = correlate(entries, skew={"warehouse": 5.0})
    assert [e["ts"] for e in timelines["a"]] == [100.0, 100.5]


def test_skew_can_reorder_lines_that_looked_out_of_order():
    entries = [line(50.0, "edge", 1, "a"), line(49.0, "warehouse", 1, "a")]
    timelines, _ = correlate(entries, skew={"warehouse": -3.0})
    assert [e["service"] for e in timelines["a"]] == ["edge", "warehouse"]


def test_same_timestamp_lines_keep_per_service_sequence_order():
    entries = [
        line(7.0, "router", 3, "a", "third"),
        line(7.0, "router", 1, "a", "first"),
        line(7.0, "router", 2, "a", "second"),
    ]
    timelines, _ = correlate(entries)
    assert [e["msg"] for e in timelines["a"]] == ["first", "second", "third"], "seq breaks timestamp ties"


def test_ties_across_services_are_deterministic_regardless_of_input_order():
    a = [line(1.0, "b-svc", 1, "x"), line(1.0, "a-svc", 1, "x")]
    t1, _ = correlate(a)
    t2, _ = correlate(list(reversed(a)))
    assert [e["service"] for e in t1["x"]] == [e["service"] for e in t2["x"]] == ["a-svc", "b-svc"]


def test_hops_count_transitions_not_distinct_services():
    entries = [line(1, "edge", 1, "a"), line(2, "api", 1, "a"), line(3, "edge", 2, "a"), line(4, "edge", 3, "a")]
    timelines, _ = correlate(entries)
    assert hops(timelines["a"]) == 2, "edge -> api -> edge is two hops even with two services"


def test_summary_and_slowest_gap():
    entries = [
        line(10.0, "edge", 1, "a"),
        line(10.5, "api", 1, "a"),
        line(12.5, "db", 1, "a", level="ERROR"),
        line(13.0, "api", 2, "a"),
        line(20.0, "edge", 1, "b"),
    ]
    timelines, _ = correlate(entries)
    assert summarize(timelines["a"]) == {"services": ["api", "db", "edge"], "hops": 3, "duration": 3.0, "errors": 1}
    assert slowest_gap(timelines["a"]) == (2.0, "api", "db")
    assert failing_requests(timelines) == ["a"]
