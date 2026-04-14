import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_closes_on_success():
    from broken import run_query
    closed = []
    class Conn:
        def execute(self, sql): return "ok"
        def close(self): closed.append(True)
    run_query(Conn(), "SELECT 1")
    assert closed == [True]

def test_closes_on_error():
    from broken import run_query
    import pytest
    closed = []
    class Conn:
        def execute(self, sql): raise ValueError("fail")
        def close(self): closed.append(True)
    with pytest.raises(RuntimeError):
        run_query(Conn(), "bad")
    assert closed == [True]
