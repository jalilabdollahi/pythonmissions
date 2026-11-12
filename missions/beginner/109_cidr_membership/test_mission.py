import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import in_subnet, is_allowed, matching_network, portal_decision


def test_address_inside_a_slash_16():
    assert in_subnet("10.20.99.1", "10.20.0.0/16") is True, "a /16 covers the whole third octet range"


def test_text_prefix_must_not_match_other_networks():
    assert in_subnet("10.1.20.5", "10.1.2.0/24") is False, "'10.1.2' is a text prefix of '10.1.20.5' but not the same network"


def test_inside_a_slash_24():
    assert in_subnet("172.16.4.200", "172.16.4.0/24") is True


def test_slash_20_boundary():
    assert in_subnet("192.168.15.255", "192.168.0.0/20") is True
    assert in_subnet("192.168.16.0", "192.168.0.0/20") is False


def test_host_bits_in_cidr_are_tolerated():
    assert in_subnet("10.20.1.1", "10.20.5.7/16") is True


def test_is_allowed_and_matching_network():
    nets = ["10.20.0.0/16", "172.16.4.0/24"]
    assert is_allowed("172.16.4.9", nets) is True
    assert is_allowed("8.8.8.8", nets) is False
    assert matching_network("172.16.4.9", nets) == "172.16.4.0/24"
    assert matching_network("8.8.8.8", nets) is None


def test_portal_decision_text():
    nets = ["10.20.0.0/16"]
    assert portal_decision("10.20.3.4", nets) == "allow 10.20.3.4 via 10.20.0.0/16"
    assert portal_decision("11.0.0.1", nets) == "deny 11.0.0.1"
