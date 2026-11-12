import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import is_severe, page_text, severe_records


def test_error_is_severe():
    assert is_severe("error")


def test_case_is_ignored():
    assert is_severe("ERROR") and is_severe("Critical")


def test_fatal_is_severe():
    assert is_severe("fatal"), "fatal is one of the severe levels"


def test_lookalike_levels_are_not_severe():
    assert not is_severe("terror_mode"), "contains 'err' but is not a level we page on"
    assert not is_severe("stderr")
    assert not is_severe("critically_low_battery_info")


def test_low_levels_are_not_severe():
    assert not is_severe("info") and not is_severe("warning")


def test_severe_records_filtering():
    records = [("info", "boot"), ("error", "db down"), ("terror_mode", "boo"), ("fatal", "oom")]
    assert severe_records(records) == [("error", "db down"), ("fatal", "oom")]


def test_page_text_uses_first_severe_message():
    assert page_text([("terror_mode", "x"), ("critical", "disk")]) == "PAGE: 1 severe record(s), first: disk"
    assert page_text([("info", "x")]) == "no page"
