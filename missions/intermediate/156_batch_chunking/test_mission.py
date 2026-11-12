import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def test_exact_multiple_gives_full_batches():
    assert list(broken.chunked(range(6), 3)) == [[0, 1, 2], [3, 4, 5]]


def test_partial_last_batch_is_kept():
    assert list(broken.chunked(range(7), 3)) == [[0, 1, 2], [3, 4, 5], [6]], "the leftover item must not be dropped"


def test_batches_are_independent_lists():
    batches = list(broken.chunked("abcde", 2))
    assert batches == [["a", "b"], ["c", "d"], ["e"]], "yielded lists must not be reused and cleared"


def test_works_with_a_generator_input():
    gen = (n * n for n in range(5))
    assert list(broken.chunked(gen, 2)) == [[0, 1], [4, 9], [16]]


def test_empty_input_yields_nothing():
    assert list(broken.chunked([], 4)) == []


def test_size_below_one_is_rejected():
    with pytest.raises(ValueError):
        list(broken.chunked([1, 2], 0))


def test_push_in_batches_sends_everything():
    calls = []
    total = broken.push_in_batches(list(range(60)), lambda b: calls.append(list(b)), size=25)
    assert total == 60
    assert [len(c) for c in calls] == [25, 25, 10]
