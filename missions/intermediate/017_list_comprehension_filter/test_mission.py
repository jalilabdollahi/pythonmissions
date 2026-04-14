import pytest
import sys
sys.path.insert(0, ".")
from broken import filter_errors, extract_ips, summarize

LINES = [
    "10.0.0.1 - - [date] ERROR disk full",
    "10.0.0.2 - - [date] INFO all good",
    "10.0.0.1 - - [date] ERROR oom",
]

def test_filter_errors():
    result = filter_errors(LINES)
    assert len(result) == 2
    assert all("ERROR" in l for l in result)

def test_extract_ips():
    errors = filter_errors(LINES)
    ips = extract_ips(errors)
    assert "10.0.0.1" in ips

def test_summarize():
    s = summarize(LINES)
    assert s["error_count"] == 2
