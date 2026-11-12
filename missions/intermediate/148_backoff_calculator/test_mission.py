import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def test_first_delay_is_the_base():
    assert broken.backoff_delay(0, base=2, factor=3, cap=100) == 2


def test_delay_grows_exponentially():
    assert broken.schedule(4, base=1, factor=2, cap=100) == [1, 2, 4, 8]


def test_delay_never_exceeds_cap():
    assert broken.schedule(8, base=1, factor=2, cap=30) == [1, 2, 4, 8, 16, 30, 30, 30], "cap must bound every delay"


def test_schedule_has_one_delay_per_retry():
    assert len(broken.schedule(5)) == 5
    assert broken.schedule(0) == []


def test_jitter_is_applied_after_the_cap():
    half = lambda d: d / 2
    assert broken.backoff_delay(10, base=1, factor=2, cap=30, jitter=half) == 15


def test_jitter_can_only_shorten_the_wait():
    rng = random.Random(7)
    delays = broken.schedule(12, base=1, factor=2, cap=30, jitter=broken.full_jitter(rng))
    assert all(0 <= d <= 30 for d in delays)


def test_total_wait_sums_capped_delays():
    assert broken.total_wait(7, base=1, factor=2, cap=10) == 1 + 2 + 4 + 8 + 10 + 10 + 10
