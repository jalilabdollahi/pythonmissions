import pytest, sys
sys.path.insert(0, ".")
from broken import sort_logs, aggregate_logs, parse_ts

LOGS_A = [
    "2024-01-01T10:00:05 INFO api: request",
    "2024-01-01T10:00:01 INFO api: start",
    "2024-01-01T10:00:10 ERROR api: crash",
]
LOGS_B = [
    "2024-01-01T10:00:03 INFO db: connect",
    "2024-01-01T10:00:07 INFO db: query",
]

def test_sort_logs():
    sorted_ = sort_logs(LOGS_A)
    ts = [parse_ts(l) for l in sorted_]
    assert ts == sorted(ts)

def test_aggregate():
    result = aggregate_logs(LOGS_A, LOGS_B)
    ts = [parse_ts(l) for l in result]
    assert ts == sorted(ts)
    assert len(result) == 5
