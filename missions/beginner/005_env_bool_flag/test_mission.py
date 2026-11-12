import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import flag_enabled, enabled_flags


def test_false_string_is_off():
    assert flag_enabled({"DEBUG": "false"}, "DEBUG") is False, 'the text "false" must not count as on'


def test_zero_string_is_off():
    assert flag_enabled({"DEBUG": "0"}, "DEBUG") is False


def test_missing_variable_is_off():
    assert flag_enabled({}, "DEBUG") is False


def test_true_spellings_are_on():
    for value in ["1", "true", "yes", "on"]:
        assert flag_enabled({"DEBUG": value}, "DEBUG") is True, value


def test_case_and_spaces_are_ignored():
    assert flag_enabled({"DEBUG": "  TRUE "}, "DEBUG") is True
    assert flag_enabled({"DEBUG": "Yes"}, "DEBUG") is True


def test_unknown_text_is_off():
    assert flag_enabled({"DEBUG": "maybe"}, "DEBUG") is False


def test_enabled_flags_keeps_order():
    env = {"A": "on", "B": "false", "C": "1"}
    assert enabled_flags(env, ["C", "B", "A"]) == ["C", "A"]
