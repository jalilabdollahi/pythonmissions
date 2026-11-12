import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from broken import pair_hosts, render_zone


def test_pairs_matching_lists():
    assert pair_hosts(["a", "b"], ["1.1.1.1", "2.2.2.2"]) == {"a": "1.1.1.1", "b": "2.2.2.2"}


def test_missing_address_is_an_error():
    with pytest.raises(ValueError):
        pair_hosts(["a", "b", "c"], ["1.1.1.1", "2.2.2.2"])


def test_extra_address_is_an_error():
    with pytest.raises(ValueError):
        pair_hosts(["a"], ["1.1.1.1", "2.2.2.2"])


def test_error_message_mentions_both_counts():
    with pytest.raises(ValueError) as info:
        pair_hosts(["a", "b", "c"], ["1.1.1.1"])
    assert "3" in str(info.value) and "1" in str(info.value), "say how many of each were given"


def test_empty_lists_give_empty_mapping():
    assert pair_hosts([], []) == {}


def test_render_zone_lines_are_sorted():
    assert render_zone({"b": "2.2.2.2", "a": "1.1.1.1"}) == ["a IN A 1.1.1.1", "b IN A 2.2.2.2"]
