# Mission 078 - Prometheus Histogram
# Fixed solution
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
    buckets=[0.1, 0.25, 0.5, 1.0, 2.5, 5.0],
)

def record_latency(duration_ms):
    LATENCY.observe(duration_ms / 1000)

def get_histogram():
    return LATENCY
