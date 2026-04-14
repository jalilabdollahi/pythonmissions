# Mission 078 - Prometheus Histogram
# Fix the 2 bugs in this script.
try:
    from prometheus_client import Histogram
except ImportError:
    class Histogram:
        def __init__(self, name, doc, buckets=None):
            self.buckets = buckets or []
            self.observations = []
        def observe(self, v): self.observations.append(v)

LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    buckets=[1.0, 0.5, 0.1, 0.25, 5.0, 2.5],  # BUG 1: not sorted ascending
)

def record_latency(duration_ms):
    """Record latency given in milliseconds."""
    LATENCY.observe(duration_ms)  # BUG 2: should convert ms to seconds (divide by 1000)

def get_histogram():
    return LATENCY
