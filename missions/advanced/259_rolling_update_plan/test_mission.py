import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from broken import Step, check_plan, describe, peak_pods, plan_rollout, resolve, resolve_limits


def test_integer_limits_are_used_as_is():
    assert resolve_limits(10, 2, 1) == (2, 1)
    assert resolve(0, 10, True) == 0


def test_surge_percentage_rounds_up():
    assert resolve_limits(10, "25%", 1)[0] == 3, "25% of 10 pods is 2.5, surge rounds up to 3"
    assert resolve_limits(5, "10%", 1)[0] == 1, "even a tiny surge percentage must allow one extra pod"
    assert resolve_limits(10, "10%", 1)[0] == 1


def test_unavailable_percentage_rounds_down():
    assert resolve_limits(10, 1, "25%")[1] == 2, "25% of 10 pods is 2.5, unavailability rounds down to 2"
    assert resolve_limits(5, 1, "10%")[1] == 0, "rounding up would allow downtime the operator did not ask for"


def test_zero_surge_and_zero_unavailable_falls_back_to_one_unavailable():
    assert resolve_limits(4, 0, 0) == (0, 1)
    assert resolve_limits(5, "5%", "5%") == (1, 0)
    steps = plan_rollout(4, 0, 0)
    assert steps[-1] == Step(0, 4, 3)


def test_known_plan_for_three_replicas_surge_one_no_downtime():
    assert plan_rollout(3, 1, 0) == [
        Step(3, 1, 3), Step(2, 1, 3), Step(2, 2, 3), Step(1, 2, 3), Step(1, 3, 3), Step(0, 3, 3),
    ]


def test_new_pods_do_not_count_as_ready_in_the_step_that_creates_them():
    steps = plan_rollout(10, "25%", "25%")
    assert steps == [Step(8, 3, 8), Step(5, 5, 8), Step(3, 8, 8), Step(0, 10, 8)]


@pytest.mark.parametrize("replicas", [1, 2, 3, 7, 10, 25])
def test_every_plan_respects_surge_and_availability(replicas):
    for surge in (0, 1, 3, "10%", "50%", "100%"):
        for unavailable in (0, 1, 2, "10%", "50%", "100%"):
            steps = plan_rollout(replicas, surge, unavailable)
            assert check_plan(replicas, steps, surge, unavailable) == [], (replicas, surge, unavailable)


def test_invalid_limits_are_rejected():
    for bad in (-1, "abc", "12.5%", True, None):
        with pytest.raises(ValueError):
            resolve_limits(5, bad, 1)
    with pytest.raises(ValueError):
        resolve_limits(0, 1, 1)
    assert describe(3, 1, 0) == "3 replicas -> 6 steps, final 3 new"
    assert peak_pods(plan_rollout(10, "25%", "25%"), 10) == 11
    assert peak_pods(plan_rollout(4, 0, 0), 4) == 4
