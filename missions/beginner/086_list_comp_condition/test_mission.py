import os, sys
sys.path.insert(0, os.path.dirname(__file__))

SERVERS = [{"name":"web-01","status":"healthy"},{"name":"web-02","status":"down"},{"name":"web-03","status":"healthy"}]

def test_returns_healthy():
    from broken import healthy_servers
    result = healthy_servers(SERVERS)
    assert "web-01" in result
    assert "web-03" in result

def test_excludes_down():
    from broken import healthy_servers
    assert "web-02" not in healthy_servers(SERVERS)

def test_returns_names():
    from broken import healthy_servers
    result = healthy_servers(SERVERS)
    assert all(isinstance(n, str) for n in result)
