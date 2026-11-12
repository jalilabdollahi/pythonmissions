import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken

DATA = [15, 20, 35, 40, 50]


def test_wikipedia_example_ranks():
    assert broken.percentile(DATA, 30) == 20
    assert broken.percentile(DATA, 40) == 20
    assert broken.percentile(DATA, 50) == 35
    assert broken.percentile(DATA, 100) == 50


def test_ceil_not_truncate_for_p95():
    samples = list(range(1, 21))
    assert broken.percentile(samples, 95) == 19, "rank = ceil(0.95 * 20) = 19"
    assert broken.percentile(samples, 99) == 20


def test_unsorted_input_gives_same_answer():
    shuffled = [50, 15, 40, 20, 35]
    assert broken.percentile(shuffled, 50) == 35
    assert broken.percentile(shuffled, 100) == 50


def test_input_list_is_not_modified():
    data = [3, 1, 2]
    broken.percentile(data, 50)
    assert data == [3, 1, 2]


def test_p_zero_returns_the_minimum():
    assert broken.percentile([9, 4, 7], 0) == 4


def test_empty_samples_and_bad_p_rejected():
    with pytest.raises(ValueError):
        broken.percentile([], 50)
    with pytest.raises(ValueError):
        broken.percentile([1], 101)


def test_latency_summary():
    samples = [120, 80, 95, 300, 110, 90, 100, 105, 85, 99]
    assert broken.latency_summary(samples) == {"p50": 99, "p95": 300, "p99": 300, "max": 300}


def test_slowest():
    assert broken.slowest([5, 9, 1, 7], 2) == [9, 7]
