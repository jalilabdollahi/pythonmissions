# Mission 043 - Prometheus Metrics Exporter
# Fix the 2 bugs in this script.
try:
    from prometheus_client import Counter, Gauge
except ImportError:
    class Counter:
        def __init__(self, name, doc, labelnames=None): self.val = 0
        def labels(self, **kw): return self
        def inc(self, amount=1): self.val += amount
    class Gauge:
        def __init__(self, name, doc): self.val = 0
        def set(self, v): self.val = v
        def inc(self, amount=1): self.val += amount
        def dec(self, amount=1): self.val -= amount

REQUEST_COUNT = Counter("http_requests_total", "Total HTTP requests", ["method", "endpoint"])
ACTIVE_CONNS = Counter("active_connections", "Active connections")  # BUG 1: should be Gauge

def record_request(method, endpoint):
    REQUEST_COUNT.labels(method=method, endpoint=endpoint).inc()

def update_connections(count):
    ACTIVE_CONNS.set(count)  # BUG 2: Counter has no .set() method

def setup_metrics():
    return REQUEST_COUNT, ACTIVE_CONNS
