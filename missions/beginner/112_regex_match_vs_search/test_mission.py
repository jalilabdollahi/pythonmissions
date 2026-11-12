import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import has_error, request_id, count_errors, error_ids

LINES = [
    "2025-03-01T10:00:00 ERROR db timeout req-4821",
    "2025-03-01T10:00:01 INFO login ok req-4822",
    "2025-03-01T10:00:02 WARN TERROR is not a level",
    "2025-03-01T10:00:03 ERROR cache miss storm req-4830",
    "ERROR started with the keyword req-1",
]


def test_error_in_the_middle_of_a_line_is_found():
    assert has_error(LINES[0]) is True, "re.match only looks at the start of the string"


def test_non_error_lines_are_not_flagged():
    assert has_error(LINES[1]) is False


def test_error_must_be_a_whole_word():
    assert has_error(LINES[2]) is False


def test_request_id_found_late_in_line():
    assert request_id(LINES[0]) == 4821


def test_missing_request_id_is_none():
    assert request_id("2025-03-01 ERROR no id here") is None


def test_count_errors():
    assert count_errors(LINES) == 3


def test_error_ids():
    assert error_ids(LINES) == [4821, 4830, 1]
