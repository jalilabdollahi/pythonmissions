# Mission 100 - Service Mesh Header Propagation
# Fix the 2 bugs in this script.

TRACE_HEADERS = ["x-request-id", "x-b3-traceid", "x-b3-spanid", "x-b3-sampled"]

def extract_trace_headers(incoming_headers):
    """Extract trace headers from incoming request headers."""
    result = {}
    for header in TRACE_HEADERS:
        if header in incoming_headers:  # BUG 1: should normalize to lowercase
            result[header] = incoming_headers[header]
    return result

def inject_headers(outgoing_headers, trace_headers):
    """Add trace headers to outgoing request."""
    outgoing_headers = trace_headers  # BUG 2: replaces instead of updating
    return outgoing_headers
