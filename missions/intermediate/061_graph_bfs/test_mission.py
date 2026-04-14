import pytest, sys
sys.path.insert(0, ".")
from broken import bfs, find_path

GRAPH = {
    "api": ["db", "cache"],
    "db": ["storage"],
    "cache": [],
    "storage": [],
}

def test_bfs():
    result = bfs(GRAPH, "api")
    assert set(result) == {"api", "db", "cache", "storage"}

def test_find_path():
    assert find_path(GRAPH, "api", "storage") is True
    assert find_path(GRAPH, "cache", "db") is False
