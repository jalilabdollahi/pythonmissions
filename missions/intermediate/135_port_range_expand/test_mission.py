import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def test_range_includes_both_ends():
    assert broken.expand_ports("8000-8003") == [8000, 8001, 8002, 8003]


def test_mixed_ports_and_ranges():
    assert broken.expand_ports("8000-8001,9000") == [8000, 8001, 9000]


def test_duplicates_removed_and_sorted():
    assert broken.expand_ports("9000, 8000,9000,8000-8001") == [8000, 8001, 9000]


def test_empty_and_whitespace():
    assert broken.expand_ports("") == []
    assert broken.expand_ports(" 22 , 80 ,") == [22, 80]


def test_port_above_65535_rejected():
    with pytest.raises(ValueError):
        broken.expand_ports("70000")
    with pytest.raises(ValueError):
        broken.expand_ports("65000-65536")


def test_port_zero_rejected():
    with pytest.raises(ValueError):
        broken.expand_ports("0-10")


def test_backwards_range_rejected():
    with pytest.raises(ValueError):
        broken.expand_ports("9003-9000")


def test_format_ports_round_trip():
    assert broken.format_ports([8000, 8001, 8002, 9000]) == "8000-8002,9000"
    assert broken.format_ports(broken.expand_ports("22,80-82,443")) == "22,80-82,443"
