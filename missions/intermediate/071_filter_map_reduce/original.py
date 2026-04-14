# Mission 071 - Filter Map Reduce Pipeline
# Fix the 2 bugs in this script.
from functools import reduce

def total_error_bytes(log_entries):
    """Sum bytes for all 5xx responses."""
    errors = filter(lambda e: e["status"] >= 500, log_entries)
    byte_counts = map(lambda e: e["bytes"], errors)
    return reduce(lambda a, b: a + b, list(byte_counts))  # BUG 1: no initial value — crashes on empty

def average_latency(entries):
    """Average latency of all entries."""
    latencies = list(map(lambda e: e["latency_ms"], entries))
    if not latencies:
        return 0.0
    total = reduce(lambda a, b: a + b, latencies, 0)
    return total / len(entries) + 1  # BUG 2: spurious +1
