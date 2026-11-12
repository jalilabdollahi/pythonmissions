import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import Coordinator, Participant


def make(**caps):
    parts = {name: Participant(name, cap) for name, cap in caps.items()}
    return parts, Coordinator(parts)


def test_all_yes_commits_everywhere():
    parts, coord = make(flights=5, hotels=5, cars=5)
    result = coord.run("t1", {"flights": 2, "hotels": 1, "cars": 1})
    assert result["status"] == "committed"
    assert [p.committed for p in parts.values()] == [2, 1, 1]
    assert coord.in_doubt() == {} and coord.decision("t1") == "commit"


def test_no_vote_aborts_and_releases_earlier_reservations():
    parts, coord = make(flights=5, hotels=0, cars=5)
    result = coord.run("t2", {"flights": 2, "hotels": 1, "cars": 1})
    assert result["status"] == "aborted" and "hotels voted no" in result["reason"]
    assert parts["flights"].available() == 5, "flights voted yes then must be rolled back"
    assert coord.in_doubt() == {}
    assert parts["cars"].reserved == {}, "cars was never asked"


def test_exception_during_prepare_is_a_no_vote_and_rolls_back():
    parts, coord = make(flights=5, hotels=5)

    def boom(txn_id, amount):
        raise TimeoutError("hotel region unreachable")

    parts["hotels"].prepare = boom
    result = coord.run("t3", {"flights": 1, "hotels": 1})
    assert result["status"] == "aborted"
    assert "hotels failed" in result["reason"]
    assert parts["flights"].reserved == {}
    assert coord.decision("t3") == "abort"


def test_decision_is_logged_before_participants_are_told():
    parts, coord = make(flights=5, hotels=5)
    seen = {}
    original = parts["flights"].commit

    def spying_commit(txn_id):
        seen["log_at_commit_time"] = list(coord.log)
        original(txn_id)

    parts["flights"].commit = spying_commit
    coord.run("t4", {"flights": 1, "hotels": 1})
    assert seen["log_at_commit_time"] == [("t4", "commit")], "log the decision BEFORE phase two"


def test_failing_commit_does_not_stop_the_other_participants():
    parts, coord = make(flights=5, hotels=5, cars=5)

    def flaky(txn_id):
        raise ConnectionError("lost connection")

    parts["flights"].commit = flaky
    result = coord.run("t5", {"flights": 1, "hotels": 1, "cars": 1})
    assert result["status"] == "committed", "decision is final once logged"
    assert result["commit_errors"] == [("flights", "lost connection")]
    assert parts["hotels"].committed == 1 and parts["cars"].committed == 1
    assert coord.in_doubt() == {"flights": ["t5"]}, "flights must be recoverable from the log"


def test_summary_reports_free_and_committed():
    parts, coord = make(flights=5, hotels=2)
    coord.run("t7", {"flights": 2, "hotels": 1})
    assert coord.summary() == {
        "flights": {"free": 3, "committed": 2},
        "hotels": {"free": 1, "committed": 1},
    }


def test_capacity_is_respected_across_concurrent_transactions():
    parts, coord = make(flights=3)
    parts["flights"].prepare("held", 2)
    result = coord.run("t6", {"flights": 2})
    assert result["status"] == "aborted"
    assert parts["flights"].reserved == {"held": 2}, "abort must not release someone else's hold"
