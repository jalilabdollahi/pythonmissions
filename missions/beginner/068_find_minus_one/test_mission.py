import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def test_error_at_start_of_line_is_detected():
    assert broken.has_error("ERROR: disk full") is True, "find() returns 0 for a match at the start"


def test_error_in_the_middle_is_detected():
    assert broken.has_error("2024-06-01 ERROR: disk full") is True


def test_clean_line_is_not_an_error():
    assert broken.has_error("INFO: all good") is False, "find() returns -1 for no match"


def test_error_lines():
    lines = ["INFO a", "ERROR b", "WARN c", "x ERROR d"]
    assert broken.error_lines(lines) == ["ERROR b", "x ERROR d"]


def test_first_error_index():
    assert broken.first_error_index(["INFO a", "ERROR b"]) == 1
    assert broken.first_error_index(["INFO a"]) == -1


def test_should_page_only_for_errors():
    assert broken.should_page(["INFO a", "INFO b"]) is False
    assert broken.should_page(["ERROR a"]) is True
