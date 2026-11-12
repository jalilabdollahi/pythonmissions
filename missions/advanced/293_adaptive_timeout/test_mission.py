import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import AdaptiveTimeout


def loaded(values, **kwargs):
    kwargs.setdefault("window", 200)
    kwargs.setdefault("floor", 0.0)
    kwargs.setdefault("ceiling", 1000.0)
    kwargs.setdefault("multiplier", 1.0)
    t = AdaptiveTimeout(**kwargs)
    for v in values:
        t.record(v)
    return t


def test_default_is_used_until_enough_samples():
    t = AdaptiveTimeout(min_samples=10, default=1.25)
    for _ in range(9):
        t.record(0.1)
    assert t.current() == 1.25


def test_p99_uses_nearest_rank():
    t = loaded(range(1, 101))
    assert t.percentile(0.99) == 99, "rank = ceil(0.99 * 100) = 99, so the 99th smallest"
    assert t.current() == 99


def test_timeout_is_p99_times_multiplier():
    t = loaded([0.2] * 20, multiplier=1.5)
    assert abs(t.current() - 0.3) < 1e-9


def test_ceiling_is_applied_after_the_multiplier():
    t = loaded([4.0] * 20, multiplier=1.5, ceiling=5.0)
    assert t.current() == 5.0


def test_floor_is_applied_after_the_multiplier():
    t = loaded([0.001] * 20, multiplier=1.5, floor=0.05)
    assert t.current() == 0.05


def test_old_samples_expire_so_timeout_recovers():
    t = AdaptiveTimeout(window=50, floor=0.0, ceiling=100, multiplier=1.0, min_samples=10)
    for _ in range(50):
        t.record(8.0)
    for _ in range(50):
        t.record(0.1)
    assert t.current() == 0.1, "a slow patch that left the window must not keep the timeout high"


def test_timeouts_widen_the_limit_during_an_incident():
    t = AdaptiveTimeout(window=50, floor=0.05, ceiling=5.0, multiplier=1.5, min_samples=10)
    for _ in range(20):
        t.settle(0.1)
    normal = t.current()
    assert abs(normal - 0.15) < 1e-9
    results = [t.settle(3.0) for _ in range(30)]
    assert results[0] is True
    assert t.current() > 1.0, "timed-out requests must feed the statistics"
    assert t.current() <= 5.0
    assert t.snapshot()["timeouts"] >= 1
