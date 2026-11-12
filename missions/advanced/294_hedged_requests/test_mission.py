import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import AllAttemptsFailed, Replica, extra_load, hedged_call, latency_saved


def test_fast_primary_sends_no_hedge():
    result = hedged_call([Replica("a", 0.5), Replica("b", 0.5)], 1.0)
    assert result.winner == "a"
    assert result.launched == 1
    assert result.finished_at == 0.5


def test_slow_primary_loses_to_the_hedge():
    result = hedged_call([Replica("a", 5.0), Replica("b", 1.0)], 1.0)
    assert result.winner == "b"
    assert result.finished_at == 2.0, "b started at t=1 and needs 1s, so it finishes at t=2"
    assert result.launched == 2
    assert result.cancelled == ["a"], "the primary is still running at t=2"


def test_response_exactly_at_the_hedge_deadline_suppresses_the_hedge():
    result = hedged_call([Replica("a", 1.0), Replica("b", 0.1)], 1.0)
    assert result.launched == 1
    assert result.winner == "a"


def test_instant_failure_does_not_win_the_race():
    result = hedged_call([Replica("a", 0.1, fail=True), Replica("b", 3.0)], 1.0)
    assert result.winner == "b"
    assert result.finished_at == 4.0


def test_cancelled_only_lists_attempts_still_in_flight():
    result = hedged_call([Replica("a", 0.2, fail=True), Replica("b", 3.0)], 1.0)
    assert result.cancelled == [], "a failed at t=0.2, there is nothing left to cancel"


def test_all_failures_raise():
    try:
        hedged_call([Replica("a", 0.1, fail=True), Replica("b", 0.2, fail=True)], 1.0)
    except AllAttemptsFailed as exc:
        assert exc.args[0] == ["a", "b"]
    else:
        raise AssertionError("when every attempt fails the call must fail")


def test_third_replica_can_win_and_cost_is_reported():
    replicas = [Replica("a", 9.0), Replica("b", 9.0), Replica("c", 0.5)]
    result = hedged_call(replicas, 2.0)
    assert result.winner == "c" and result.finished_at == 4.5
    assert result.cancelled == ["a", "b"]
    assert extra_load(replicas, 2.0) == 2
    assert latency_saved(replicas, 2.0) == 4.5
