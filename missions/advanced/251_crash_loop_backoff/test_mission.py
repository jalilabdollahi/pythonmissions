import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import RestartPolicy, Supervised, simulate


def actions(decisions):
    return [(d.action, d.delay) for d in decisions]


def test_backoff_doubles_on_consecutive_quick_crashes():
    policy = RestartPolicy(base_delay=1.0, max_delay=30.0, max_crashes=10)
    result = simulate(policy, [(1, 1)] * 4)
    assert actions(result) == [("restart", 1.0), ("restart", 2.0), ("restart", 4.0), ("restart", 8.0)]


def test_backoff_is_capped():
    policy = RestartPolicy(base_delay=1.0, max_delay=10.0, max_crashes=99, window=1e9)
    result = simulate(policy, [(1, 1)] * 7)
    assert [d.delay for d in result] == [1.0, 2.0, 4.0, 8.0, 10.0, 10.0, 10.0]


def test_long_uptime_resets_the_backoff():
    policy = RestartPolicy(base_delay=1.0, stable_after=60.0, max_crashes=10)
    result = simulate(policy, [(1, 1), (1, 1), (1, 1), (120, 1), (1, 1)])
    assert [d.delay for d in result] == [1.0, 2.0, 4.0, 1.0, 2.0], (
        "a process that ran for a minute and then crashed starts a fresh backoff sequence"
    )


def test_uptime_exactly_stable_after_counts_as_stable():
    policy = RestartPolicy(base_delay=1.0, stable_after=60.0, max_crashes=10)
    result = simulate(policy, [(1, 1), (60, 1)])
    assert [d.delay for d in result] == [1.0, 1.0]


def test_crash_loop_gives_up_and_marks_failed():
    policy = RestartPolicy(max_crashes=3, window=100.0, base_delay=1.0)
    proc = Supervised("billing-worker", policy)
    decisions = []
    for t in (10, 20, 30):
        proc.started(t - 1)
        decisions.append(proc.exited(2, t))
    assert [d.action for d in decisions] == ["restart", "restart", "give_up"]
    assert proc.state == "failed"
    assert proc.describe()["recent_crashes"] == 3


def test_crashes_outside_the_window_do_not_count():
    policy = RestartPolicy(max_crashes=2, window=100.0, stable_after=1e9)
    proc = Supervised("w", policy)
    proc.started(0)
    assert proc.exited(1, 50).action == "restart"
    proc.started(51)
    assert proc.exited(1, 150).action == "restart", "the crash at t=50 is exactly one window old and has expired"
    proc.started(151)
    assert proc.exited(1, 200).action == "give_up", "crashes at t=150 and t=200 are both inside the window"


def test_clean_exit_follows_the_policy_mode():
    on_failure = simulate(RestartPolicy(mode="on-failure"), [(5, 0)])
    assert [(d.action, d.reason) for d in on_failure] == [("stop", "clean exit")]
    always = simulate(RestartPolicy(mode="always"), [(5, 0), (5, 0), (5, 3)])
    assert [d.action for d in always] == ["restart", "restart", "restart"]
    assert always[0].delay == 0.0
    never = simulate(RestartPolicy(mode="never"), [(5, 1)])
    assert never[0].action == "stop"
