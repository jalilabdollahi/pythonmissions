import pytest, sys
sys.path.insert(0, ".")
from broken import TaskQueue

def test_priority_order():
    q = TaskQueue()
    q.push("low", 1)
    q.push("high", 10)
    q.push("medium", 5)
    assert q.pop() == "high"
    assert q.pop() == "medium"
    assert q.pop() == "low"

def test_peek():
    q = TaskQueue()
    q.push("urgent", 100)
    assert q.peek() == "urgent"
    q.pop()
    assert q.peek() is None
