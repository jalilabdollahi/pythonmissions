import pytest, sys
sys.path.insert(0, ".")
from broken import parse_multiline_logs

LOGS = """ERROR NullPointerException at Service.java:42
    at com.example.Service.process(Service.java:42)
    at com.example.Main.main(Main.java:10)
INFO Server started on port 8080
WARN High memory usage: 85%
    Consider increasing heap size
"""

def test_entry_count():
    entries = parse_multiline_logs(LOGS)
    assert len(entries) == 3

def test_trace_attached():
    entries = parse_multiline_logs(LOGS)
    error_entry = next(e for e in entries if "NullPointer" in e["message"])
    assert len(error_entry["trace"]) == 2

def test_simple_entry():
    entries = parse_multiline_logs(LOGS)
    info_entry = next(e for e in entries if "Server started" in e["message"])
    assert info_entry["trace"] == []
