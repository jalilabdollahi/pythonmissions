import pytest, sys
sys.path.insert(0, ".")
from broken import total_error_bytes, average_latency

ENTRIES = [
    {"status": 200, "bytes": 1024, "latency_ms": 10},
    {"status": 500, "bytes": 512,  "latency_ms": 200},
    {"status": 503, "bytes": 256,  "latency_ms": 500},
]

def test_total_error_bytes():
    assert total_error_bytes(ENTRIES) == 768

def test_total_error_bytes_empty():
    assert total_error_bytes([{"status": 200, "bytes": 100}]) == 0

def test_average_latency():
    assert average_latency(ENTRIES) == (10 + 200 + 500) / 3
