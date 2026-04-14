import pytest, sys
sys.path.insert(0, ".")
from broken import parse_prometheus_text, get_metric

PROM_TEXT = """# HELP http_requests_total Total requests
# TYPE http_requests_total counter
http_requests_total{method="GET"} 1234
http_requests_total{method="POST"} 567
active_connections 42
"""

def test_parse_skips_comments():
    m = parse_prometheus_text(PROM_TEXT)
    assert "#" not in m

def test_parse_values():
    m = parse_prometheus_text(PROM_TEXT)
    assert m.get("active_connections") == 42.0

def test_get_metric():
    assert get_metric(PROM_TEXT, "active_connections") == 42.0
    assert get_metric(PROM_TEXT, "nonexistent", 0.0) == 0.0
