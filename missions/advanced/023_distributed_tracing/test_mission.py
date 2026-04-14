import pytest, sys
sys.path.insert(0, ".")
from broken import TraceCorrelator

SPANS = [
    {"span_id": "root", "parent_span_id": None, "start_time": 0, "end_time": 100},
    {"span_id": "child1", "parent_span_id": "root", "start_time": 10, "end_time": 60},
    {"span_id": "child2", "parent_span_id": "root", "start_time": 20, "end_time": 90},
]

def test_build_tree():
    tc = TraceCorrelator()
    for s in SPANS: tc.add_span(s)
    roots = tc.build_tree()
    assert len(roots) == 1
    assert len(roots[0]["children"]) == 2

def test_span_duration():
    tc = TraceCorrelator()
    for s in SPANS: tc.add_span(s)
    tc.build_tree()
    assert tc.span_duration_ms("root") == 100
    assert tc.span_duration_ms("child1") == 50

def test_critical_path():
    tc = TraceCorrelator()
    for s in SPANS: tc.add_span(s)
    tc.build_tree()
    cp = tc.critical_path("root")
    assert cp == 170  # root(100) + child2(70)
