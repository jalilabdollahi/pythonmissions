import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def test_no_outages_means_no_downtime():
    assert broken.downtime_minutes([], 0, 100) == 0


def test_single_outage():
    assert broken.downtime_minutes([(10, 40)], 0, 100) == 30


def test_overlapping_outages_counted_once():
    assert broken.downtime_minutes([(10, 60), (30, 90)], 0, 100) == 80, "minutes 30-60 must not be counted twice"


def test_outage_contained_in_another():
    assert broken.downtime_minutes([(10, 90), (20, 30), (40, 50)], 0, 100) == 80


def test_adjacent_outages_add_up():
    assert broken.downtime_minutes([(0, 10), (10, 25)], 0, 100) == 25


def test_outage_is_clamped_to_reporting_period():
    assert broken.downtime_minutes([(-50, 20), (90, 500)], 0, 100) == 30


def test_unsorted_input_order_does_not_matter():
    a = broken.downtime_minutes([(50, 70), (0, 20), (10, 55)], 0, 100)
    b = broken.downtime_minutes([(0, 20), (10, 55), (50, 70)], 0, 100)
    assert a == b == 70


def test_uptime_percent_is_the_complement():
    assert broken.uptime_percent([(0, 50)], 0, 1000) == 95.0
    assert broken.uptime_percent([], 0, 1000) == 100.0
    assert broken.uptime_percent([(10, 60), (30, 90)], 0, 1000) == 92.0


def test_empty_period_rejected_and_worst_outage():
    with pytest.raises(ValueError):
        broken.uptime_percent([], 5, 5)
    assert broken.worst_outage([(0, 5), (10, 40)]) == (10, 40)
