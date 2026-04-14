import pytest
import sys
sys.path.insert(0, ".")
from broken import write_report, format_metric

def test_write_report_has_header():
    metrics = [{"service": "api", "requests": 100, "errors": 5, "latency_ms": "12.3"}]
    output = write_report(metrics)
    assert "service" in output
    assert "requests" in output

def test_write_report_data():
    metrics = [{"service": "worker", "requests": 50, "errors": 0, "latency_ms": "5.0"}]
    output = write_report(metrics)
    assert "worker" in output
    assert "50" in output
