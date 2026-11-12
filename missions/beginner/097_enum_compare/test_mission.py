import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import Level, parse_level, should_page, to_wire, most_severe


def test_parse_level_returns_enum_member():
    assert parse_level("warn") is Level.WARN


def test_parse_level_is_tolerant_of_case_and_spaces():
    assert parse_level(" ERROR ") is Level.ERROR


def test_parse_level_rejects_unknown_text():
    with pytest.raises(ValueError):
        parse_level("fatal")


def test_error_pages():
    assert should_page("error") is True, "convert the raw string to a Level before comparing"


def test_other_levels_do_not_page():
    assert should_page("warn") is False
    assert should_page("debug") is False


def test_to_wire_returns_plain_string():
    assert to_wire(Level.ERROR) == "error", "send .value over the wire, not the member"
    assert isinstance(to_wire(Level.DEBUG), str)


def test_most_severe():
    assert most_severe(["debug", "error", "warn"]) is Level.ERROR
    assert most_severe(["debug"]) is Level.DEBUG
    assert most_severe([]) is None
