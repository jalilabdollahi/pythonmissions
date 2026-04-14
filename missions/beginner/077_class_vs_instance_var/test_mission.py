import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_independent_timeouts():
    from broken import Connection
    c1 = Connection("db-01", 10)
    c2 = Connection("db-02", 60)
    assert c1.timeout == 10
    assert c2.timeout == 60

def test_describe():
    from broken import Connection
    c = Connection("db-01", 10)
    assert "10" in c.describe()
