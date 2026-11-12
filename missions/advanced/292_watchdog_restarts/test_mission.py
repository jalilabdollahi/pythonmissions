import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import Watchdog, run_probes


def make(results, threshold=3, cooldown=300, restart=None, start=100):
    clock = {"now": start}
    probes = iter(results)
    restarts = []
    hook = restart or (lambda: restarts.append(clock["now"]))
    dog = Watchdog(lambda: next(probes), hook, lambda: clock["now"], threshold, cooldown)
    return dog, clock, restarts


def test_three_consecutive_failures_trigger_a_restart():
    dog, clock, restarts = make([False, False, False])
    assert run_probes(dog, clock, 3) == ["degraded", "degraded", "restarted"]
    assert restarts == [160], "first restart must not wait for the cooldown"
    assert dog.restarts == 1


def test_a_healthy_probe_resets_the_streak():
    dog, clock, restarts = make([False, False, True, False, False, True])
    outcomes = run_probes(dog, clock, 6)
    assert "restarted" not in outcomes, "failures were never three in a row"
    assert restarts == []


def test_cooldown_blocks_a_restart_storm():
    dog, clock, restarts = make([False] * 20, cooldown=300)
    outcomes = run_probes(dog, clock, 14, interval=30)
    assert outcomes.count("restarted") == 2, outcomes
    assert "cooling_down" in outcomes
    assert restarts[1] - restarts[0] >= 300


def test_streak_restarts_from_zero_after_a_restart():
    results = [False, False, False, True, False]
    dog, clock, restarts = make(results, cooldown=10)
    run_probes(dog, clock, 3)
    clock["now"] += 500
    assert dog.tick() == "healthy"
    clock["now"] += 500
    assert dog.tick() == "degraded", "one new failure is not enough for another restart"
    assert dog.restarts == 1


def test_failure_streak_after_restart_needs_fresh_evidence():
    dog, clock, _ = make([False, False, False, False], cooldown=300)
    run_probes(dog, clock, 3)
    clock["now"] += 1000
    assert dog.tick() == "degraded"
    assert dog.status()["consecutive_failures"] == 1


def test_crashing_restart_hook_is_contained_and_cooled_down():
    def broken_hook():
        raise RuntimeError("systemctl exploded")

    dog, clock, _ = make([False] * 8, restart=broken_hook, cooldown=300)
    outcomes = run_probes(dog, clock, 6)
    assert outcomes[2] == "restart_failed"
    assert outcomes.count("restart_failed") == 1, "the cooldown applies to failed attempts too"
    assert dog.restart_errors == ["systemctl exploded"]
    assert dog.restarts == 0


def test_flapping_service_is_flagged():
    dog, clock, _ = make([False] * 40, cooldown=60)
    run_probes(dog, clock, 30, interval=40)
    assert dog.is_flapping(window=3600, limit=3)
    assert dog.status()["flapping"] is True
