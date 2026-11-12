import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import tally, top_codes, error_share, digest_line

CODES = [200, 200, 404, 200, 500, 404, 200, 301]


def test_tally_counts_repeats():
    counts = tally(CODES)
    assert counts[200] == 4, "each repeat must add one to the count"
    assert counts[404] == 2
    assert counts[500] == 1


def test_tally_of_empty_list():
    assert dict(tally([])) == {}


def test_top_codes_most_frequent_first():
    assert top_codes(CODES, 2) == [(200, 4), (404, 2)]


def test_top_codes_n_larger_than_distinct_codes():
    assert len(top_codes(CODES, 10)) == 4


def test_top_codes_n_one():
    assert top_codes(CODES, 1) == [(200, 4)]


def test_error_share():
    assert error_share(CODES) == 3 / 8
    assert error_share([]) == 0.0


def test_digest_line():
    assert digest_line(CODES, 3) == "200:4 404:2 500:1"
