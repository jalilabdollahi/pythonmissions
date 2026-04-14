import pytest, sys
sys.path.insert(0, ".")
from broken import inject_trace_context, generate_trace_id, format_traceparent

def test_trace_id_length():
    tid = generate_trace_id()
    assert len(tid) == 32  # 16 bytes = 32 hex chars

def test_traceparent_format():
    tp = format_traceparent("a" * 32, "b" * 16)
    assert tp.startswith("00-")
    parts = tp.split("-")
    assert len(parts) == 4

def test_inject():
    headers = {"Content-Type": "application/json"}
    inject_trace_context(headers)
    assert "traceparent" in headers
    assert "Traceparent" not in headers or headers.get("Traceparent") == headers.get("traceparent")
