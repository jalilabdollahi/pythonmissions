import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import Endpoint, register, unique


def test_identical_endpoints_are_equal():
    assert Endpoint("a", 1) == Endpoint("a", 1), "define __eq__ so equal data means equal objects"


def test_different_port_or_host_is_not_equal():
    assert Endpoint("a", 1) != Endpoint("a", 2)
    assert Endpoint("a", 1) != Endpoint("b", 1)


def test_endpoint_is_not_equal_to_other_types():
    assert Endpoint("a", 1) != ("a", 1)
    assert Endpoint("a", 1) != "a:1"


def test_in_operator_finds_equal_endpoint():
    assert Endpoint("a", 1) in [Endpoint("z", 9), Endpoint("a", 1)]


def test_equal_endpoints_collapse_in_a_set():
    assert len({Endpoint("a", 1), Endpoint("a", 1), Endpoint("b", 1)}) == 2, "equal objects must hash equal"


def test_register_rejects_duplicates():
    reg = []
    assert register(reg, Endpoint("a", 1)) is True
    assert register(reg, Endpoint("a", 1)) is False
    assert len(reg) == 1


def test_unique_keeps_first_seen_order():
    items = [Endpoint("b", 2), Endpoint("a", 1), Endpoint("b", 2)]
    assert unique(items) == [Endpoint("b", 2), Endpoint("a", 1)]
