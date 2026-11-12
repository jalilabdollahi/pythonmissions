import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from broken import fit_trend, plan, predict, recent_window, replicas_needed, seconds_until

# Epoch-sized timestamps: the line is v = 5 + 0.01 * (t - 1_700_000_000)
T0 = 1_700_000_000
LINE = [(T0 + dt, 5 + 0.01 * dt) for dt in (0, 100, 250, 400)]


def test_fit_recovers_slope_exactly():
    slope, _ = fit_trend(LINE)
    assert slope == pytest.approx(0.01)


def test_prediction_uses_intercept_at_absolute_time():
    assert predict(LINE, T0 + 1000) == pytest.approx(15.0), "the line must pass through the mean point"


def test_noisy_samples_pass_through_the_centroid():
    pts = [(0, 1.0), (10, 4.0), (20, 4.0), (30, 8.0)]
    slope, intercept = fit_trend(pts)
    assert slope == pytest.approx(0.21)
    assert slope * 15 + intercept == pytest.approx(4.25), "least squares line crosses (mean_t, mean_v)"


def test_degenerate_inputs_are_rejected():
    with pytest.raises(ValueError):
        fit_trend([(1, 1.0)])
    with pytest.raises(ValueError):
        fit_trend([(5, 1.0), (5, 2.0)])


def test_window_includes_sample_exactly_on_the_boundary():
    pts = [(100, 1), (200, 2), (300, 3), (400, 4)]
    assert recent_window(pts, now=400, span=200) == [(200, 2), (300, 3), (400, 4)]


def test_flat_trend_never_reaches_limit_and_does_not_crash():
    flat = [(0, 5.0), (60, 5.0), (120, 5.0)]
    assert seconds_until(flat, 10.0, now=120) is None


def test_falling_trend_never_reaches_limit_and_already_above_returns_zero():
    falling = [(0, 9.0), (60, 8.0), (120, 7.0)]
    assert seconds_until(falling, 20.0, now=120) is None
    assert seconds_until(falling, 6.0, now=120) == 0.0, "already past the limit means zero, not negative"


def test_time_until_limit_on_rising_trend():
    pts = [(0, 0.0), (100, 2.0), (200, 4.0)]
    assert seconds_until(pts, 10.0, now=200) == pytest.approx(300.0)


def test_headroom_means_replicas_run_below_full_capacity():
    # 16 cores at 4 cores per replica with 25% headroom: 3 usable cores each -> 6 replicas
    assert replicas_needed(16, 4.0, headroom=0.25) == 6
    assert replicas_needed(0.1, 4.0) == 2, "never go below the minimum"


def test_plan_end_to_end():
    pts = [(0, 4.0), (300, 6.0), (600, 8.0), (900, 10.0), (-5000, 99.0)]
    result = plan(pts, now=900, horizon=600, per_replica=5.0, span=1000)
    assert result["samples"] == 4
    assert result["expected_load"] == pytest.approx(14.0)
    assert result["replicas"] == 4
