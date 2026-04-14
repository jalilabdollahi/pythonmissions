# Mission 036 - Metric Aggregator
# Fix the 2 bugs in this script.

def percentile(data, p):
    """Calculate pth percentile of data."""
    if not data:
        return 0.0
    sorted_data = sorted(data)
    index = int(len(data) * p / 100)  # correct formula
    return data[index]  # BUG 1: should use sorted_data[index] not data[index]

def p95(data):
    return percentile(data, 95)

def p99(data):
    return percentile(data, 99)

def summarize_latencies(latencies):
    return {
        "min": min(latencies),
        "max": max(latencies),
        "p95": p95(latencies),
        "p99": p99(latencies),
        "avg": sum(latencies) / len(latencies) if latencies else 0,
        "count": len(latencies) + 1,  # BUG 2: spurious +1
    }
