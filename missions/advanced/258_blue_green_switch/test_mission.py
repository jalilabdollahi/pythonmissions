import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from broken import BlueGreenRouter, NothingToRollBack


def scripted(results):
    calls = []
    it = iter(results)

    def check(color):
        calls.append(color)
        return next(it, True)

    check.calls = calls
    return check


def test_deploy_goes_to_the_idle_color_and_leaves_live_traffic_alone():
    router = BlueGreenRouter("v1")
    assert router.deploy("v2") == "green"
    assert router.live_version() == "v1", "deploying must never touch the color serving users"
    assert router.status() == {"active": "blue", "live_version": "v1", "idle_version": "v2", "can_rollback": False}


def test_healthy_candidate_is_switched_after_required_consecutive_checks():
    router = BlueGreenRouter("v1")
    router.deploy("v2")
    check = scripted([])
    result = router.cutover(check, required=3)
    assert (result.status, result.active, result.checks) == ("switched", "green", 3)
    assert check.calls == ["green"] * 3, "checks run against the idle color and stop once the gate is satisfied"
    assert router.live_version() == "v2"


def test_failed_check_resets_the_streak():
    router = BlueGreenRouter("v1")
    router.deploy("v2")
    result = router.cutover(scripted([True, True, False, True, True]), required=3, max_checks=5)
    assert result.status == "blocked", "only two healthy checks in a row at the end; one earlier failure resets the count"
    assert router.active == "blue"
    result = router.cutover(scripted([True, True, False, True, True, True]), required=3, max_checks=6)
    assert (result.status, result.checks) == ("switched", 6)


def test_blocked_cutover_never_calls_verify_or_changes_state():
    router = BlueGreenRouter("v1")
    router.deploy("v2")
    verified = []
    result = router.cutover(scripted([False] * 10), verify=lambda c: verified.append(c) or True)
    assert result.status == "blocked" and verified == []
    assert router.status()["can_rollback"] is False
    assert router.history[-1][0] == "blocked"


def test_failed_post_switch_verification_rolls_back_automatically():
    router = BlueGreenRouter("v1")
    router.deploy("v2")
    result = router.cutover(scripted([]), verify=lambda color: False)
    assert result.status == "rolled_back" and result.active == "blue"
    assert router.live_version() == "v1", "traffic must be back on the old color"
    assert router.status()["can_rollback"] is False, "nothing is left to roll back after an automatic rollback"
    with pytest.raises(NothingToRollBack):
        router.rollback()


def test_manual_rollback_works_once():
    router = BlueGreenRouter("v1")
    router.deploy("v2")
    router.cutover(scripted([]))
    assert router.rollback() == "blue"
    assert router.live_version() == "v1"
    with pytest.raises(NothingToRollBack):
        router.rollback()
    assert router.live_version() == "v1", "a second rollback must not flip traffic back to the bad color"


def test_second_release_reuses_the_old_color():
    router = BlueGreenRouter("v1")
    router.deploy("v2")
    router.cutover(scripted([]))
    assert router.deploy("v3") == "blue"
    assert router.live_version() == "v2"
    router.cutover(scripted([]))
    assert router.live_version() == "v3" and router.active == "blue"
    assert [h[0] for h in router.history] == ["deploy", "switch", "deploy", "switch"]


def test_cutover_requires_a_deployed_candidate():
    router = BlueGreenRouter("v1")
    with pytest.raises(ValueError):
        router.cutover(scripted([]))
