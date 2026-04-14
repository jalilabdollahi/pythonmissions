import pytest, sys
sys.path.insert(0, ".")
from broken import trace_request

def test_trace_returns_span():
    span = trace_request("GET", "/api/health", 200)
    assert span is not None

def test_span_ended():
    span = trace_request("POST", "/deploy", 201)
    assert span.ended is True

def test_span_attributes():
    span = trace_request("GET", "/api/v1/users", 200)
    assert span.attrs.get("http.method") == "GET"
    assert span.attrs.get("http.status_code") == 200
