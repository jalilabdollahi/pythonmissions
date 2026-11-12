import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import total_usage, matches_invoice, mismatches


def test_total_of_volumes():
    assert total_usage([10.5, 20.25]) == 30.75


def test_classic_float_sum_matches():
    assert matches_invoice([0.1, 0.2], 0.3) is True, "0.1 + 0.2 is not exactly 0.3 in floating point"


def test_many_small_volumes_match():
    assert matches_invoice([0.1] * 10, 1.0) is True


def test_real_difference_is_a_mismatch():
    assert matches_invoice([0.1, 0.2], 0.35) is False


def test_mismatches_are_sorted_and_tolerant():
    customers = {
        "zeta": ([5.0], 6.0),
        "acme": ([0.1, 0.2], 0.3),
        "beta": ([1.1, 2.2], 3.3),
        "delta": ([9.0], 8.0),
    }
    assert mismatches(customers) == ["delta", "zeta"]
