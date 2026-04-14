import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_inserts_at_front():
    from broken import push_priority
    q = ["routine-deploy", "health-check"]
    push_priority(q, "hotfix-payment")
    assert q[0] == "hotfix-payment"

def test_length_increases():
    from broken import push_priority
    q = ["a", "b"]
    push_priority(q, "x")
    assert len(q) == 3

def test_others_shift_right():
    from broken import push_priority
    q = ["a", "b"]
    push_priority(q, "x")
    assert q == ["x", "a", "b"]
