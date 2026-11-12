import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import name_column_width, slowest_pipelines

TIMINGS = {
    "etl-orders": [120, 130, 125],
    "etl-users": [30, 40],
    "ml-train": [900],
    "reports": [60, 60, 60],
}


def test_slowest_pipeline_comes_first():
    assert slowest_pipelines(TIMINGS, 1) == ["ml-train"]


def test_top_n_limits_and_orders_results():
    assert slowest_pipelines(TIMINGS, 3) == ["ml-train", "etl-orders", "reports"]


def test_top_n_larger_than_data():
    assert slowest_pipelines({"only": [1]}, 5) == ["only"]


def test_name_column_width_is_longest_name():
    assert name_column_width(TIMINGS) == len("etl-orders")


def test_name_column_width_for_no_pipelines():
    assert name_column_width({}) == 0
