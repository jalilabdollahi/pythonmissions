import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from broken import Autoscaler, Metric, bound_reason, desired_replicas, metric_proposal


def cpu(value, target=50):
    return Metric("cpu", value, target)


def test_scales_proportionally_and_rounds_up():
    assert desired_replicas(4, [cpu(100)], max_replicas=20) == 8
    assert desired_replicas(4, [cpu(60)], max_replicas=20) == 5, "4 * 1.2 = 4.8 must round up to 5"
    assert desired_replicas(10, [cpu(20)], max_replicas=20) == 4


def test_float_noise_does_not_add_a_replica():
    metric = Metric("rps", 2.1, 0.7)
    assert metric_proposal(2, metric, 0.1) == 6, "2 * (2.1 / 0.7) is 6.000000000000001 in floating point"


def test_inside_the_tolerance_band_nothing_changes_including_the_edges():
    for value in (46, 50, 54, 55, 45):
        assert desired_replicas(6, [cpu(value)]) == 6, value
    assert desired_replicas(6, [cpu(56)]) == 7
    assert desired_replicas(6, [cpu(44)]) == 6 * 44 // 50 + 1


def test_the_most_demanding_metric_wins():
    metrics = [cpu(25), Metric("memory", 90, 60), Metric("queue", 10, 10)]
    assert desired_replicas(4, metrics, max_replicas=20) == 6


def test_metrics_without_data_are_ignored():
    metrics = [Metric("rps", None, 100), cpu(100)]
    assert desired_replicas(4, metrics, max_replicas=20) == 8
    assert desired_replicas(4, [Metric("rps", None, 100)]) == 4, "no data at all means keep the current size"
    assert desired_replicas(6, [Metric("rps", None, 100), cpu(50)]) == 6, "missing data is not a zero reading"


def test_result_is_clamped_to_min_and_max():
    assert desired_replicas(5, [cpu(1)], min_replicas=3, max_replicas=8) == 3
    assert desired_replicas(5, [cpu(500)], min_replicas=3, max_replicas=8) == 8
    assert desired_replicas(0, [cpu(50)], min_replicas=2, max_replicas=8) == 2


def test_invalid_configuration_is_rejected():
    with pytest.raises(ValueError):
        desired_replicas(3, [cpu(10)], min_replicas=5, max_replicas=2)
    with pytest.raises(ValueError):
        desired_replicas(3, [Metric("cpu", 10, 0)])


def test_scale_down_waits_for_the_stabilization_window_but_scale_up_is_immediate():
    scaler = Autoscaler(1, 20, stabilization=300.0)
    assert scaler.decide(10, [cpu(100)], now=0) == 20
    assert scaler.history_summary() == {"samples": 1, "highest": 20, "lowest": 20}
    assert scaler.decide(20, [cpu(25)], now=60) == 20, "a recent higher recommendation holds the size up"
    assert scaler.decide(20, [cpu(25)], now=360) == 10, "the old recommendation (t=0) has expired, t=60 still counts"
    assert scaler.decide(20, [cpu(25)], now=700) == 10
    assert scaler.explain(10, [cpu(100), Metric("rps", None, 5)]) == ["cpu: 20 replicas", "rps: no data"]


def test_a_single_decision_cannot_more_than_double_the_fleet():
    scaler = Autoscaler(1, 100)
    assert scaler.decide(3, [cpu(500)], now=0) == 7
    assert scaler.decide(10, [cpu(500)], now=10) == 20
    assert Autoscaler.scale_up_ceiling(1) == 5


def test_bound_reason_explains_the_decision():
    assert bound_reason(5, [cpu(50)], 2, 8) == "steady"
    assert bound_reason(5, [cpu(1)], 3, 8) == "min bound"
    assert bound_reason(5, [cpu(500)], 3, 8) == "max bound"
    assert bound_reason(5, [cpu(100)], 3, 20) == "metrics"
