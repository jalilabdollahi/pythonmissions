import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_len_empty():
    from broken import TaskQueue
    q = TaskQueue()
    assert len(q) == 0

def test_len_after_add():
    from broken import TaskQueue
    q = TaskQueue()
    q.add("deploy")
    q.add("test")
    assert len(q) == 2

def test_len_after_pop():
    from broken import TaskQueue
    q = TaskQueue()
    q.add("deploy")
    q.pop()
    assert len(q) == 0
