import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

import broken


def test_valid_number_is_parsed():
    assert broken.parse_retries("5") == 5


def test_garbage_text_falls_back_to_default():
    assert broken.parse_retries("abc") == 3


def test_custom_default_is_used():
    assert broken.parse_retries("", default=1) == 1


def test_none_is_not_swallowed():
    with pytest.raises(TypeError):
        broken.parse_retries(None)


def test_load_settings_defaults_region():
    assert broken.load_settings({"retries": "2"}) == {"retries": 2, "region": "eu-west"}


def test_load_settings_does_not_hide_missing_value():
    with pytest.raises(TypeError):
        broken.load_settings({"retries": None})


def test_effective_attempts():
    assert broken.effective_attempts({"retries": "4"}) == 5
