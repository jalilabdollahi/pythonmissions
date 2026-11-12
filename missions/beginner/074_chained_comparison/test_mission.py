import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def test_middle_value_is_partial():
    assert broken.is_partial(60) is True, "0 < 60 < 100 is a partial load"


def test_over_100_is_not_partial():
    assert broken.is_partial(150) is False


def test_boundaries_are_not_partial():
    assert broken.is_partial(0) is False
    assert broken.is_partial(100) is False


def test_negative_is_not_partial():
    assert broken.is_partial(-5) is False


def test_classify_labels():
    assert [broken.classify(v) for v in (-1, 0, 50, 100, 101)] == ["invalid", "idle", "partial", "full", "invalid"]


def test_candidates():
    assert broken.candidates({"n3": 99, "n1": 1, "n2": 0, "n4": 100, "n5": 140}) == ["n1", "n3"]


def test_summary_counts():
    assert broken.summary({"a": 0, "b": 5, "c": 6}) == {"idle": 1, "partial": 2}
