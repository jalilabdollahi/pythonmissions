import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import fill_label, pool_line, report


def test_seven_eighths():
    assert fill_label(7, 8) == "87.5%"


def test_one_third_rounds_to_one_decimal():
    assert fill_label(1, 3) == "33.3%"


def test_full_and_empty_pools():
    assert fill_label(10, 10) == "100.0%"
    assert fill_label(0, 10) == "0.0%"


def test_pool_line_format():
    assert pool_line("ssd-a", 7, 8) == "ssd-a: 87.5%"


def test_report_is_sorted_by_name():
    assert report({"ssd-a": (7, 8), "hdd-b": (1, 3)}) == ["hdd-b: 33.3%", "ssd-a: 87.5%"]
