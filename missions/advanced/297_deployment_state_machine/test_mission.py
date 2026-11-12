import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import TRANSITIONS, Deployment, IllegalTransition, in_flight, reachable


def make(deploy_id="rel-1"):
    ticks = iter(range(100, 200))
    return Deployment(deploy_id, lambda: next(ticks))


def test_happy_path_records_every_state():
    d = make()
    for event in ("start", "deployed", "verified"):
        assert d.apply(event) is True
    assert d.path() == ["queued", "deploying", "verifying", "live"]
    assert d.history[-1] == ("live", 103)


def test_verification_cannot_be_skipped():
    d = make()
    d.apply("start")
    assert not d.can_move("live")
    try:
        d.move("live")
    except IllegalTransition:
        pass
    else:
        raise AssertionError("deploying -> live must be illegal")


def test_legality_depends_on_the_current_state():
    d = make()
    assert not d.can_move("live"), "queued -> live is not an edge even though live is a real state"
    assert not d.can_move("rolled_back")
    assert d.can_move("deploying")


def test_illegal_move_leaves_the_deployment_untouched():
    d = make()
    d.apply("start")
    before = (d.state, list(d.history))
    try:
        d.move("rolled_back")
    except IllegalTransition:
        pass
    assert (d.state, d.history) == before, "a rejected move must not change anything"


def test_duplicate_event_is_a_noop():
    d = make()
    d.apply("start")
    assert d.apply("deployed") is True
    assert d.apply("deployed") is False, "at-least-once delivery repeats events"
    assert d.path() == ["queued", "deploying", "verifying"]


def test_failure_leads_to_rollback_and_terminal_states_are_final():
    d = make()
    for event in ("start", "error", "rollback", "rollback_done"):
        d.apply(event)
    assert d.state == "rolled_back" and d.is_terminal()
    for target in TRANSITIONS:
        if target != "rolled_back":
            assert not d.can_move(target)


def test_unknown_state_raises_value_error_and_helpers_work():
    d = make()
    try:
        d.move("exploded")
    except ValueError:
        pass
    else:
        raise AssertionError("unknown states are programming errors")
    assert reachable("failed") == {"rolling_back", "rolled_back", "rollback_failed"}
    live = make("live-one")
    for event in ("start", "deployed", "verified"):
        live.apply(event)
    assert in_flight([d, live]) == ["rel-1"]
