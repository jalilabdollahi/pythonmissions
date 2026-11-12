import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import count_errors, error_bytes, error_rate, count_slow, render

RECORDS = [
    {"status": 200, "bytes": 5000, "ms": 40},
    {"status": 404, "bytes": 300, "ms": 15},
    {"status": 500, "bytes": 120, "ms": 900},
    {"status": 503, "bytes": 80, "ms": 1500},
]


def test_count_errors_counts_rows_not_bytes():
    assert count_errors(RECORDS) == 2, "count matches with sum(1 for ...), not their sizes"


def test_status_500_itself_is_an_error():
    assert count_errors([{"status": 500, "bytes": 1}]) == 1


def test_no_errors_gives_zero():
    assert count_errors([{"status": 200, "bytes": 99}]) == 0


def test_error_bytes_sums_only_error_rows():
    assert error_bytes(RECORDS) == 200


def test_error_rate_is_a_fraction():
    assert error_rate(RECORDS) == 0.5
    assert error_rate([]) == 0.0


def test_count_slow_counts_requests_over_limit():
    assert count_slow(RECORDS, 800) == 2
    assert count_slow(RECORDS, 900) == 1, "exactly at the limit is not slow"


def test_render_line():
    assert render(RECORDS) == "2/4 errors (50.0%)"
