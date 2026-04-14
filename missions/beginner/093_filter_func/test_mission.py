import os, sys
sys.path.insert(0, os.path.dirname(__file__))

CONTAINERS = [
    {"id":"c1","status":"running"},
    {"id":"c2","status":"stopped"},
    {"id":"c3","status":"running"},
]

def test_returns_list():
    from broken import running_containers
    assert isinstance(running_containers(CONTAINERS), list)

def test_excludes_stopped():
    from broken import running_containers
    result = running_containers(CONTAINERS)
    assert all(c["status"] != "stopped" for c in result)

def test_count():
    from broken import running_containers
    assert len(running_containers(CONTAINERS)) == 2
