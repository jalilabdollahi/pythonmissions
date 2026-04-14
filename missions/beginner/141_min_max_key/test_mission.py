import os, sys
sys.path.insert(0, os.path.dirname(__file__))

PODS = [
    {"name":"pod-a","memory_mb":512,"cpu":20},
    {"name":"pod-b","memory_mb":2048,"cpu":80},
    {"name":"pod-c","memory_mb":256,"cpu":5},
]

def test_heaviest():
    from broken import heaviest
    assert heaviest(PODS)["name"] == "pod-b"

def test_lightest():
    from broken import lightest
    assert lightest(PODS)["name"] == "pod-c"
