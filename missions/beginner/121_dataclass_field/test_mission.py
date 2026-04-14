import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_creates_instance():
    from broken import Server
    s = Server("web-01", "localhost", 8080)
    assert s.name == "web-01"

def test_default_tags():
    from broken import Server
    s = Server("web-01", "localhost", 8080)
    assert s.tags == []

def test_independent_tags():
    from broken import Server
    s1 = Server("web-01", "localhost", 8080)
    s2 = Server("web-02", "localhost", 8081)
    s1.tags.append("prod")
    assert s2.tags == []
