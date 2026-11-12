import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def make():
    return broken.LatencyHistogram([1.0, 0.1, 0.5])


def test_bounds_are_sorted_and_labelled():
    h = make()
    assert list(h.snapshot()) == ["0.1", "0.5", "1.0", "+Inf"]


def test_buckets_are_cumulative():
    h = make()
    for v in (0.05, 0.3, 0.7):
        h.observe(v)
    snap = h.snapshot()
    assert snap["0.1"] == 1
    assert snap["0.5"] == 2, "the 0.5 bucket includes everything in the 0.1 bucket"
    assert snap["1.0"] == 3


def test_boundary_value_belongs_to_its_own_bucket():
    h = make()
    h.observe(0.5)
    snap = h.snapshot()
    assert snap["0.1"] == 0
    assert snap["0.5"] == 1, "le means less than or equal"
    assert snap["1.0"] == 1


def test_plus_inf_bucket_holds_everything():
    h = make()
    for v in (0.05, 2.0, 9.5):
        h.observe(v)
    snap = h.snapshot()
    assert snap["+Inf"] == 3
    assert snap["1.0"] == 1


def test_count_total_and_mean():
    h = make()
    for v in (1.0, 2.0, 3.0):
        h.observe(v)
    assert h.count == 3
    assert h.total == 6.0
    assert h.mean() == 2.0
    assert make().mean() == 0.0


def test_empty_histogram_all_zero():
    assert make().snapshot() == {"0.1": 0, "0.5": 0, "1.0": 0, "+Inf": 0}


def test_render_lines_end_with_sum_and_count():
    h = make()
    h.observe(0.2)
    lines = broken.render_buckets("http_req", h)
    assert lines[0] == 'http_req_bucket{le="0.1"} 0'
    assert 'http_req_bucket{le="+Inf"} 1' in lines
    assert lines[-1] == "http_req_count 1"
