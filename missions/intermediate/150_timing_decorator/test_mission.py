import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


class FakeClock:
    def __init__(self, *ticks):
        self.ticks = list(ticks)

    def __call__(self):
        return self.ticks.pop(0)


def test_wrapper_returns_the_function_result():
    sink = []

    @broken.timed(sink, clock=FakeClock(0, 1))
    def extract(n):
        return n * 2

    assert extract(21) == 42, "the decorator must not swallow the return value"


def test_records_name_and_elapsed():
    sink = []

    @broken.timed(sink, clock=FakeClock(10, 12.5))
    def transform():
        return None

    transform()
    assert sink == [("transform", 2.5)]


def test_each_call_is_measured_from_its_own_start():
    sink = []

    @broken.timed(sink, clock=FakeClock(0, 1, 100, 103))
    def load():
        pass

    load()
    load()
    assert [s for _, s in sink] == [1, 3], "start time must be taken per call, not at decoration time"


def test_default_clock_is_monotonic(monkeypatch):
    ticks = iter([0.0, 0.25])
    monkeypatch.setattr(time, "perf_counter", lambda: next(ticks))
    monkeypatch.setattr(time, "monotonic", lambda: next(ticks), raising=False)
    wall = iter([500.0, 400.0])
    monkeypatch.setattr(time, "time", lambda: next(wall))
    sink = []

    @broken.timed(sink)
    def stage():
        pass

    stage()
    assert sink[0][1] == 0.25, "use a monotonic clock, wall time can go backwards"


def test_slowest_and_totals():
    sink = [("a", 1.0), ("b", 4.0), ("a", 2.0)]
    assert broken.slowest(sink) == "b"
    assert broken.total_by_stage(sink) == {"a": 3.0, "b": 4.0}
    assert broken.slowest([]) is None
