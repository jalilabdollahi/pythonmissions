import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_first_occurrence():
    from broken import count_event
    counts = {}
    count_event(counts, "deploy")
    assert counts["deploy"] == 1

def test_increments():
    from broken import count_event
    counts = {}
    count_event(counts, "deploy")
    count_event(counts, "deploy")
    assert counts["deploy"] == 2

def test_two_events():
    from broken import count_event
    counts = {}
    count_event(counts, "deploy")
    count_event(counts, "rollback")
    assert counts["deploy"] == 1
    assert counts["rollback"] == 1
