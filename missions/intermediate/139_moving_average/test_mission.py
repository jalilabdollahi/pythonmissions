import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def test_window_two_hand_checked():
    assert broken.moving_average([10, 20, 30, 40], 2) == [10.0, 15.0, 25.0, 35.0]


def test_window_contains_exactly_n_values():
    out = broken.moving_average([0, 0, 0, 30, 0, 0], 3)
    assert out == [0.0, 0.0, 0.0, 10.0, 10.0, 10.0], "the spike must leave the window after 3 samples"


def test_early_values_use_only_available_samples():
    out = broken.moving_average([8, 8, 8], 5)
    assert out == [8.0, 8.0, 8.0], "do not divide by the window size while it is still filling"


def test_window_one_is_identity():
    assert broken.moving_average([3, 1, 4], 1) == [3.0, 1.0, 4.0]


def test_rounding_to_two_decimals():
    assert broken.moving_average([1, 1, 2], 3) == [1.0, 1.0, 1.33]


def test_invalid_window_and_empty_input():
    with pytest.raises(ValueError):
        broken.moving_average([1, 2], 0)
    assert broken.moving_average([], 3) == []


def test_spike_requires_strictly_greater_than_limit():
    values = [100, 100, 100, 100]
    assert broken.spike_indices(values, 2, 100) == [], "equal to the limit is not above it"
    assert broken.spike_indices([100, 200, 200], 2, 150) == [2]


def test_latest_trend():
    assert broken.latest_trend([1, 2, 9], 2) == "rising"
    assert broken.latest_trend([9, 9, 1], 2) == "falling"
