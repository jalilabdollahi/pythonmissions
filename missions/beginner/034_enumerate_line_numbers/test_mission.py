import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import error_report, format_summary

LOG = [
    "INFO boot ok",
    "ERROR disk full on /var",
    "INFO retrying",
    "WARN slow response",
    "ERROR timeout talking to db",
]


def test_first_line_error_is_line_one():
    assert error_report(["ERROR first"]) == ["line 1: ERROR first"], "line numbers start at 1"


def test_report_lists_correct_numbers():
    assert error_report(LOG) == [
        "line 2: ERROR disk full on /var",
        "line 5: ERROR timeout talking to db",
    ]


def test_no_errors_gives_empty_report():
    assert error_report(["INFO a", "WARN b"]) == []


def test_summary_counts_errors():
    assert format_summary(LOG) == "2 error(s)"
