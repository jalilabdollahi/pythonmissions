import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


@pytest.mark.parametrize("code,expected", [
    (100, "informational"), (199, "informational"),
    (200, "success"), (204, "success"), (299, "success"),
    (301, "redirect"), (399, "redirect"),
    (400, "client_error"), (404, "client_error"), (499, "client_error"),
    (500, "server_error"), (599, "server_error"),
    (99, "unknown"), (600, "unknown"), (0, "unknown"),
])
def test_classify_boundaries(code, expected):
    assert broken.classify(code) == expected, "check the edges of the %s range" % expected


def test_200_is_success():
    assert broken.classify(200) == "success", "ranges are half-open: 200 <= code < 300"


def test_600_is_not_a_server_error():
    assert broken.classify(600) == "unknown"


def test_numeric_strings_from_logs_are_accepted():
    assert broken.classify("404") == "client_error"
    assert broken.classify("200") == "success"


def test_summarize_counts_each_class():
    assert broken.summarize([200, "200", 301, 404, 500, 503]) == {
        "success": 2, "redirect": 1, "client_error": 1, "server_error": 2,
    }


def test_error_rate():
    assert broken.error_rate([200, 200, 500, 599]) == 0.5
    assert broken.error_rate([]) == 0.0
    assert broken.error_rate([600, 200]) == 0.0


def test_retryable_codes():
    assert broken.is_retryable(429) and broken.is_retryable(408) and broken.is_retryable("503")
    assert not broken.is_retryable(501) and not broken.is_retryable(404) and not broken.is_retryable(200)
