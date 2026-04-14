# Mission 071 - Filter Map Reduce Pipeline
# Fixed solution
from functools import reduce

def total_error_bytes(log_entries):
    errors = filter(lambda e: e["status"] >= 500, log_entries)
    byte_counts = map(lambda e: e["bytes"], errors)
    return reduce(lambda a, b: a + b, list(byte_counts), 0)

def average_latency(entries):
    latencies = list(map(lambda e: e["latency_ms"], entries))
    if not latencies:
        return 0.0
    total = reduce(lambda a, b: a + b, latencies, 0)
    return total / len(entries)
