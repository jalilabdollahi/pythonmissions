import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken
from broken import RollingWindows, sustained_spike


def test_five_samples_size_three_gives_three_windows():
    assert list(RollingWindows([1, 2, 3, 4, 5], 3)) == [(1, 2, 3), (2, 3, 4), (3, 4, 5)]


def test_last_complete_window_is_included():
    assert list(RollingWindows([1, 2, 3], 3)) == [(1, 2, 3)], "a window that exactly fits is complete"


def test_too_few_samples_gives_no_windows():
    assert list(RollingWindows([1, 2], 3)) == []


def test_for_loop_ends_cleanly():
    seen = []
    for window in RollingWindows([5, 6, 7, 8], 2):
        seen.append(window)
    assert seen == [(5, 6), (6, 7), (7, 8)]


def test_can_be_iterated_twice():
    windows = RollingWindows([1, 2, 3, 4], 2)
    first = list(windows)
    second = list(windows)
    assert first == second == [(1, 2), (2, 3), (3, 4)]


def test_len_matches_number_of_windows():
    windows = RollingWindows(range(10), 4)
    assert len(windows) == len(list(windows)) == 7


def test_sustained_spike_detection():
    assert sustained_spike([10, 20, 90, 95, 99], 3, 90)
    assert not sustained_spike([10, 20, 90, 95, 99], 3, 99)


def test_limit_is_inclusive():
    assert sustained_spike([10, 10, 10], 3, 10), "an average exactly at the limit counts as a spike"


def test_peak_window():
    assert RollingWindows([1], 1) is not None
    assert broken.peak_window([1, 9, 8, 2], 2) == (9, 8)
    assert broken.peak_window([1], 3) is None


def test_size_must_be_positive():
    import pytest

    with pytest.raises(ValueError):
        broken.RollingWindows([1], 0)
