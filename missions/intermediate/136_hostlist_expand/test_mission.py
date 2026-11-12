import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def test_plain_host():
    assert broken.expand_hostlist("db1") == ["db1"]


def test_range_is_inclusive():
    assert broken.expand_hostlist("web[1-3]") == ["web1", "web2", "web3"]


def test_zero_padding_preserved():
    assert broken.expand_hostlist("web[01-03].dc1") == ["web01.dc1", "web02.dc1", "web03.dc1"]


def test_padding_crossing_a_digit_boundary():
    assert broken.expand_hostlist("n[08-11]") == ["n08", "n09", "n10", "n11"]


def test_list_and_range_inside_brackets():
    assert broken.expand_hostlist("web[01-02,07]") == ["web01", "web02", "web07"]


def test_commas_inside_brackets_do_not_split_patterns():
    assert broken.expand_hostlist("web[1,3],db1") == ["web1", "web3", "db1"]


def test_unbalanced_brackets_rejected():
    with pytest.raises(ValueError):
        broken.expand_hostlist("web[1-3")
    with pytest.raises(ValueError):
        broken.expand_hostlist("web1-3]")
