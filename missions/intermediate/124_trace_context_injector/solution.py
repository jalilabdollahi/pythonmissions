# Mission 124 - Trace Context HTTP Injector
# Fixed solution
import secrets

def generate_trace_id():
    return secrets.token_hex(16)

def generate_span_id():
    return secrets.token_hex(8)

def format_traceparent(trace_id, span_id, sampled=True):
    flags = "01" if sampled else "00"
    return f"00-{trace_id}-{span_id}-{flags}"

def inject_trace_context(headers, trace_id=None, span_id=None):
    trace_id = trace_id or generate_trace_id()
    span_id = span_id or generate_span_id()
    traceparent = format_traceparent(trace_id, span_id)
    headers["traceparent"] = traceparent
    return headers
