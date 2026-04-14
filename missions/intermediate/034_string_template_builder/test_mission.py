import pytest
import sys
sys.path.insert(0, ".")
from broken import build_alert

def test_build_alert():
    result = build_alert("CRITICAL", "payment-svc", "prod-01", "disk full")
    assert "CRITICAL" in result
    assert "payment-svc" in result
    assert "prod-01" in result
    assert "disk full" in result

def test_alert_format():
    result = build_alert("WARNING", "api", "web-01", "high latency")
    assert result.startswith("ALERT [WARNING]")
