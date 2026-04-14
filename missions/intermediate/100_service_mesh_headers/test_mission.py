import pytest, sys
sys.path.insert(0, ".")
from broken import extract_trace_headers, inject_headers

def test_case_insensitive():
    headers = {"X-Request-Id": "abc123", "Content-Type": "application/json"}
    result = extract_trace_headers(headers)
    assert result.get("x-request-id") == "abc123"

def test_inject_preserves_existing():
    outgoing = {"Content-Type": "application/json", "Authorization": "Bearer xyz"}
    trace = {"x-request-id": "req-001"}
    result = inject_headers(outgoing, trace)
    assert result["Content-Type"] == "application/json"
    assert result["x-request-id"] == "req-001"
