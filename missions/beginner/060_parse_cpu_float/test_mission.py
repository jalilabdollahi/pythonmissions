import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def test_parse_whole_percentage():
    assert broken.parse_cpu("80%") == 80.0


def test_parse_fractional_percentage():
    assert broken.parse_cpu("12.5%") == 12.5, "decimal text cannot go through int()"


def test_parse_ignores_spaces():
    assert broken.parse_cpu(" 7 % ") == 7.0


def test_hottest_pod():
    assert broken.hottest({"a": "10.5%", "b": "10.9%", "c": "3%"}) == "b"


def test_average_keeps_fraction():
    assert broken.average_cpu({"a": "10.5%", "b": "20%"}) == 15.25


def test_scale_up_threshold():
    assert broken.needs_scale_up({"a": "73.5%", "b": "76.5%"}) is False
    assert broken.needs_scale_up({"a": "75.5%", "b": "76.5%"}) is True
