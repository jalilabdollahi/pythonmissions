import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import is_valid_ip, ip_family, split_valid, summarize


def test_valid_ipv4_is_accepted():
    assert is_valid_ip("192.168.1.10") is True


def test_ipv6_is_accepted():
    assert is_valid_ip("2001:db8::1") is True, "use ipaddress.ip_address so both versions work"


def test_junk_returns_false_instead_of_raising():
    assert is_valid_ip("not-an-ip") is False


def test_out_of_range_octet_is_invalid():
    assert is_valid_ip("256.1.1.1") is False


def test_spaces_are_ignored():
    assert is_valid_ip("  10.0.0.1 ") is True


def test_ip_family():
    assert ip_family("10.0.0.1") == 4
    assert ip_family("::1") == 6
    assert ip_family("nope") is None


def test_split_valid_keeps_order_and_originals():
    good, bad = split_valid([" 10.0.0.1", "bad", "::1", "1.2.3"])
    assert good == ["10.0.0.1", "::1"]
    assert bad == ["bad", "1.2.3"]


def test_summarize():
    assert summarize(["10.0.0.1", "2001:db8::1", "oops"]) == "2 accepted, 1 rejected"
