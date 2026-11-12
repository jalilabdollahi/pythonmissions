import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from broken import Sample, analyze, evaluate_rollout, format_verdict, gate, latency_regressed, percentile, z_score


def test_clearly_worse_canary_is_rolled_back():
    verdict = analyze(Sample(2000, 20), Sample(2000, 90))
    assert verdict.decision == "rollback"
    assert verdict.baseline_rate == 0.01 and verdict.canary_rate == 0.045


def test_similar_error_rates_are_promoted():
    verdict = analyze(Sample(3000, 30), Sample(3000, 33))
    assert verdict.decision == "promote"


def test_too_little_traffic_on_either_side_is_inconclusive():
    assert analyze(Sample(100, 0), Sample(5000, 400)).decision == "inconclusive", "baseline is too small"
    assert analyze(Sample(5000, 50), Sample(100, 30)).decision == "inconclusive", "canary is too small"
    assert analyze(Sample(5000, 50), Sample(500, 5)).decision != "inconclusive"


def test_unequal_traffic_uses_the_pooled_standard_error():
    baseline, canary = Sample(5000, 50), Sample(500, 10)
    assert z_score(baseline, canary) == pytest.approx(2.05, abs=0.01)
    assert analyze(baseline, canary).decision == "rollback", "pooled z is 2.05, above the 1.96 threshold"


def test_zero_variance_does_not_crash():
    assert analyze(Sample(1000, 0), Sample(1000, 0)).decision == "promote"
    verdict = analyze(Sample(1000, 1000), Sample(1000, 1000))
    assert verdict.decision == "promote" and verdict.z == 0.0


def test_a_better_canary_is_never_rolled_back():
    verdict = analyze(Sample(1000, 100), Sample(1000, 20))
    assert verdict.decision == "promote"
    assert verdict.z < -5, "negative z means the canary has fewer errors"


def test_significant_but_tiny_difference_is_ignored():
    verdict = analyze(Sample(1_000_000, 1000), Sample(1_000_000, 1100))
    assert verdict.z > 1.96
    assert verdict.decision == "promote", "0.01 percentage points is below the minimum effect size"


def test_invalid_samples_are_rejected():
    with pytest.raises(ValueError):
        analyze(Sample(100, 101), Sample(100, 0))
    with pytest.raises(ValueError):
        analyze(Sample(100, -1), Sample(100, 0))


def test_rollout_stops_at_first_rollback_and_waits_when_inconclusive():
    ok = (Sample(1000, 10), Sample(1000, 11))
    bad = (Sample(2000, 20), Sample(2000, 90))
    small = (Sample(10, 0), Sample(10, 0))
    assert evaluate_rollout([ok, bad, ok])[0] == "rollback"
    assert len(evaluate_rollout([ok, bad, ok])[1]) == 2
    assert evaluate_rollout([ok, small])[0] == "wait"
    assert evaluate_rollout([small, ok])[0] == "promote"
    assert evaluate_rollout([])[0] == "wait"
    assert format_verdict(analyze(*ok)).startswith("PROMOTE: baseline 1.00%, canary 1.10%")


def test_latency_gate_catches_slow_canaries_that_have_clean_error_rates():
    base_ms = [100 + i for i in range(100)]
    slow_ms = [150 + i for i in range(100)]
    assert percentile(base_ms, 95) == 194
    assert latency_regressed(base_ms, slow_ms) is True
    assert latency_regressed(base_ms, base_ms) is False
    ok = (Sample(1000, 10), Sample(1000, 10))
    verdict = gate(*ok, base_ms, slow_ms)
    assert (verdict.decision, verdict.reason) == ("rollback", "p95 latency regressed")
    assert gate(*ok, base_ms, base_ms).decision == "promote"
