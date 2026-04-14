# Mission 124 - Trace Context HTTP Injector
# Fix the 2 bugs in this script.
import secrets

def generate_trace_id():
    return secrets.token_hex(8)  # BUG 1: trace ID should be 16 bytes = 32 hex chars

def generate_span_id():
    return secrets.token_hex(8)  # span ID is 8 bytes = 16 hex chars (correct)

def format_traceparent(trace_id, span_id, sampled=True):
    flags = "01" if sampled else "00"
    return f"00-{trace_id}-{span_id}-{flags}"

def inject_trace_context(headers, trace_id=None, span_id=None):
    """Add W3C traceparent header to the headers dict."""
    trace_id = trace_id or generate_trace_id()
    span_id = span_id or generate_span_id()
    traceparent = format_traceparent(trace_id, span_id)
    headers["traceparent"] = traceparent  # BUG 2: header name should be "traceparent" (lowercase) — actually this is correct
    headers["Traceparent"] = traceparent  # BUG 2 actual: duplicate/wrong casing
    return headers
