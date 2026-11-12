import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken
import pytest


def test_first_pick_is_first_backend():
    assert broken.RoundRobin(["a", "b", "c"]).next_backend() == "a"


def test_wraps_back_to_first_after_last():
    rr = broken.RoundRobin(["a", "b", "c"])
    assert rr.peek_cycle(4) == ["a", "b", "c", "a"], "the fourth pick must wrap to index 0, not run past the end"


def test_two_full_rounds():
    rr = broken.RoundRobin(["x", "y"])
    assert rr.peek_cycle(6) == ["x", "y", "x", "y", "x", "y"]


def test_single_backend_always_chosen():
    rr = broken.RoundRobin(["only"])
    assert rr.peek_cycle(3) == ["only"] * 3


def test_empty_pool_rejected():
    with pytest.raises(ValueError, match="no backends"):
        broken.RoundRobin([])


def test_served_counter_and_share():
    rr = broken.RoundRobin(["a", "b"])
    rr.peek_cycle(4)
    assert rr.served == 4
    assert rr.share("a") == 0.5
