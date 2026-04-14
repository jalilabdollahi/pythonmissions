import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_returns_on_success():
    from broken import retry_loop
    calls = []
    def fn(a):
        calls.append(1)
        return "ok" if len(calls) == 2 else None
    assert retry_loop(5, fn) == "ok"

def test_returns_none_on_all_fail():
    from broken import retry_loop
    assert retry_loop(3, lambda a: None) is None

def test_calls_correct_times():
    from broken import retry_loop
    calls = []
    retry_loop(3, lambda a: calls.append(1) or None)
    assert len(calls) == 3
