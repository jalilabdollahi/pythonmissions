import pytest, sys
sys.path.insert(0, ".")
from broken import top_k_errors, top_error_service

COUNTS = {"api": 500, "db": 200, "cache": 50, "worker": 300}

def test_top_k():
    result = top_k_errors(COUNTS, 2)
    names = [r[0] for r in result]
    assert names[0] == "api"
    assert names[1] == "worker"

def test_top_service():
    assert top_error_service(COUNTS) == "api"

def test_empty():
    assert top_k_errors({}, 3) == []
