import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import build_tree, render, self_time, self_times, time_by_service, walk


def span(id, parent, service, start, end, name="op"):
    return {"id": id, "parent": parent, "service": service, "name": name, "start": start, "end": end}


SIMPLE = [
    span("root", None, "web", 0, 100),
    span("db", "root", "db", 10, 40),
    span("cache", "root", "cache", 50, 60),
]


def test_sequential_children_subtract_their_durations():
    times = self_times(build_tree(SIMPLE))
    assert times == {"root": 60, "db": 30, "cache": 10}


def test_children_are_ordered_by_start_time():
    spans = [
        span("r", None, "web", 0, 100),
        span("late_short", "r", "a", 50, 55),
        span("early_long", "r", "b", 10, 90),
    ]
    root = build_tree(spans)[0]
    assert [c["id"] for c in root["children"]] == ["early_long", "late_short"]


def test_parallel_children_are_not_double_counted():
    spans = [
        span("r", None, "gateway", 0, 100),
        span("a", "r", "inventory", 10, 70),
        span("b", "r", "pricing", 20, 80),
    ]
    times = self_times(build_tree(spans))
    assert times["r"] == 30, "children overlap during 20-70; the parent was waiting for 10-80 only"
    assert times["r"] >= 0


def test_nested_overlap_inside_another_child_is_absorbed():
    spans = [
        span("r", None, "gateway", 0, 100),
        span("a", "r", "x", 10, 90),
        span("b", "r", "y", 20, 30),
    ]
    assert self_times(build_tree(spans))["r"] == 20


def test_child_running_past_its_parent_is_clipped():
    spans = [span("r", None, "web", 0, 50), span("c", "r", "slow", 40, 120)]
    assert self_times(build_tree(spans))["r"] == 40, "only 40-50 of the child counts against the parent"


def test_orphan_spans_become_roots():
    spans = SIMPLE + [span("lost", "missing-parent", "mail", 5, 25)]
    roots = build_tree(spans)
    assert sorted(r["id"] for r in roots) == ["lost", "root"]
    assert {n["id"] for n in walk(roots)} == {"root", "db", "cache", "lost"}


def test_time_by_service_adds_up_to_wall_time():
    spans = SIMPLE + [span("db2", "root", "db", 70, 90)]
    totals = time_by_service(build_tree(spans))
    assert totals == {"web": 40, "db": 50, "cache": 10}
    assert sum(totals.values()) == 100


def test_render_shows_indentation_and_self_time():
    out = render(build_tree(SIMPLE))
    assert out.splitlines()[0] == "web:op 100ms (self 60ms)"
    assert out.splitlines()[1] == "  db:op 30ms (self 30ms)"
    assert self_time(build_tree(SIMPLE)[0]) == 60
