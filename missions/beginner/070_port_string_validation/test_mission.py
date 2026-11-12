import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

import broken


def test_valid_ports_are_returned_as_int():
    assert broken.validate_port("80") == 80
    assert broken.validate_port("65535") == 65535
    assert broken.validate_port("1") == 1


def test_port_zero_is_rejected():
    with pytest.raises(ValueError):
        broken.validate_port("0")


def test_port_above_65535_is_rejected():
    with pytest.raises(ValueError):
        broken.validate_port("65536")


@pytest.mark.parametrize("text", ["8_0", "+80", "-5", "", "abc", " 80", "80.0"])
def test_non_digit_text_is_rejected(text):
    with pytest.raises(ValueError):
        broken.validate_port(text)


def test_port_list():
    assert broken.parse_port_list("80, 443") == [80, 443]


def test_port_list_with_bad_entry_fails():
    with pytest.raises(ValueError):
        broken.parse_port_list("80,0")


def test_open_rules():
    assert broken.open_rules("22,8080") == ["allow tcp 22", "allow tcp 8080"]
