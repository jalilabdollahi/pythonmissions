import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken

LOG = [
    "2025-03-01 10:00:00,100 INFO worker started",
    "2025-03-01 10:00:01,200 ERROR payment call failed",
    "Traceback (most recent call last):",
    '  File "pay.py", line 9, in charge',
    "Caused by: gateway ERROR 503 from upstream",
    "2025-03-01 10:00:02,300 WARN retry budget low",
    "2025-03-01 10:00:03,400 WARNING queue depth high",
    "2025-03-01 10:00:04,500 FATAL out of disk",
    "2025-03-01 10:00:05,600 DEBUG tick",
]


def test_full_count_of_levels():
    counts = broken.count_levels(LOG)
    assert counts == {"DEBUG": 1, "INFO": 1, "WARNING": 2, "ERROR": 1, "CRITICAL": 1}


def test_trace_line_mentioning_error_is_not_an_entry():
    lines = [
        "2025-03-01 10:00:01,200 ERROR boom",
        "Caused by: upstream ERROR 500 and INFO leak",
    ]
    counts = broken.count_levels(lines)
    assert counts["ERROR"] == 1, "continuation lines must not be counted as new entries"
    assert counts["INFO"] == 0


def test_message_text_does_not_change_the_level():
    lines = ["2025-03-01 10:00:01,200 INFO recovered from ERROR state"]
    counts = broken.count_levels(lines)
    assert counts["INFO"] == 1 and counts["ERROR"] == 0


def test_warn_is_counted_as_warning():
    counts = broken.count_levels(["2025-03-01 10:00:02,300 WARN low disk"])
    assert counts["WARNING"] == 1


def test_fatal_is_counted_as_critical():
    counts = broken.count_levels(["2025-03-01 10:00:04,500 FATAL out of disk"])
    assert counts["CRITICAL"] == 1


def test_all_levels_present_even_when_zero():
    assert broken.count_levels([]) == dict.fromkeys(
        ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], 0
    )


def test_continuation_lines_listed():
    assert len(broken.continuation_lines(LOG)) == 3
