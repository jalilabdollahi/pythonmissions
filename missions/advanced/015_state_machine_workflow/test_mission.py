import pytest, sys
sys.path.insert(0, ".")
from broken import StateMachine

TRANSITIONS = {
    ("pending", "start"): {"to": "running", "guard": None},
    ("running", "succeed"): {"to": "passed", "guard": None},
    ("running", "fail"): {"to": "failed", "guard": None},
    ("running", "approve"): {"to": "approved", "guard": lambda ctx: ctx.get("approved")},
}

def test_valid_transition():
    sm = StateMachine("pending", TRANSITIONS)
    assert sm.trigger("start") is True
    assert sm.state == "running"

def test_invalid_transition():
    sm = StateMachine("pending", TRANSITIONS)
    assert sm.trigger("fail") is False
    assert sm.state == "pending"

def test_guard_blocks():
    sm = StateMachine("running", TRANSITIONS)
    assert sm.trigger("approve", {"approved": False}) is False
    assert sm.state == "running"

def test_guard_allows():
    sm = StateMachine("running", TRANSITIONS)
    assert sm.trigger("approve", {"approved": True}) is True
    assert sm.state == "approved"

def test_can_trigger_unknown():
    sm = StateMachine("pending", TRANSITIONS)
    assert sm.can_trigger("nonexistent") is False
