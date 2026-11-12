import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import coverage, downsample, fill_forward, gap_count


def test_samples_land_in_the_bucket_that_contains_them():
    points = [(0, 1), (50, 3), (65, 5), (119, 7)]
    assert downsample(points, 60) == [(0, 2.0), (60, 6.0)], "timestamp 50 belongs to bucket 0"


def test_buckets_align_to_the_epoch_not_the_first_sample():
    series = downsample([(970, 4), (1010, 6)], 60)
    assert series == [(960, 5.0)], "1000 // 60 * 60 is 960"


def test_empty_buckets_are_reported_as_gaps():
    series = downsample([(0, 1), (200, 2)], 60, agg="sum")
    assert series == [(0, 1), (60, None), (120, None), (180, 2)]
    assert gap_count(series) == 2
    assert coverage(series) == 0.5


def test_average_is_not_truncated():
    assert downsample([(0, 1), (1, 2)], 60) == [(0, 1.5)]


def test_last_uses_timestamp_order_not_arrival_order():
    points = [(50, 9), (10, 1), (30, 5)]
    assert downsample(points, 60, agg="last") == [(0, 9)]


def test_start_is_inclusive_and_end_is_exclusive():
    points = [(0, 1), (60, 2), (120, 3)]
    assert downsample(points, 60, agg="sum", start=60, end=120) == [(60, 2)]
    assert downsample([], 60) == []


def test_aggregators_and_validation():
    points = [(0, 4), (10, 8), (20, 2)]
    assert downsample(points, 60, agg="max") == [(0, 8)]
    assert downsample(points, 60, agg="min") == [(0, 2)]
    try:
        downsample(points, 0)
    except ValueError:
        pass
    else:
        raise AssertionError("step 0 must raise ValueError")


def test_fill_forward_is_limited():
    series = [(0, 5), (60, None), (120, None), (180, 7)]
    assert fill_forward(series, max_gap=1) == [(0, 5), (60, 5), (120, None), (180, 7)]
