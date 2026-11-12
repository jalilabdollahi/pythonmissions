import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def test_plain_counter():
    item = broken.parse_statsd("api.hits:3|c")
    assert item == {"name": "api.hits", "type": "c", "value": 3, "delta": False}


def test_sampled_counter_is_scaled_up():
    item = broken.parse_statsd("api.hits:1|c|@0.1")
    assert item["value"] == pytest.approx(10), "a 10% sample rate means each datagram stands for 10 events"


def test_gauge_absolute_vs_delta():
    absolute = broken.parse_statsd("queue:5|g")
    relative_down = broken.parse_statsd("queue:-5|g")
    relative_up = broken.parse_statsd("queue:+2|g")
    assert absolute["delta"] is False and absolute["value"] == 5
    assert relative_down["delta"] is True and relative_down["value"] == -5
    assert relative_up["delta"] is True and relative_up["value"] == 2


def test_fractional_timer_value():
    item = broken.parse_statsd("db.query:12.5|ms")
    assert item["value"] == 12.5


def test_unsupported_and_malformed_lines():
    for bad in ("nocolon", "x:1", "x:1|h", "x:abc|c", ":1|c"):
        with pytest.raises(ValueError):
            broken.parse_statsd(bad)


def test_aggregate_mixes_all_types():
    lines = [
        "hits:1|c|@0.5",
        "hits:2|c",
        "depth:10|g",
        "depth:-3|g",
        "depth:+1|g",
        "lat:5.5|ms",
        "lat:7|ms",
    ]
    out = broken.aggregate(lines)
    assert out["counters"] == {"hits": pytest.approx(4)}
    assert out["gauges"] == {"depth": 8}
    assert out["timers"] == {"lat": [5.5, 7]}


def test_gauge_set_after_delta_replaces_value():
    out = broken.aggregate(["g:5|g", "g:-1|g", "g:20|g"])
    assert out["gauges"]["g"] == 20
