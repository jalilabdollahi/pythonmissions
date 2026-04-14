# Mission 100 - Service Mesh Header Propagation
# Fixed solution

TRACE_HEADERS = ["x-request-id", "x-b3-traceid", "x-b3-spanid", "x-b3-sampled"]

def extract_trace_headers(incoming_headers):
    normalized = {k.lower(): v for k, v in incoming_headers.items()}
    result = {}
    for header in TRACE_HEADERS:
        if header in normalized:
            result[header] = normalized[header]
    return result

def inject_headers(outgoing_headers, trace_headers):
    result = dict(outgoing_headers)
    result.update(trace_headers)
    return result
