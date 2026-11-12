# Mission 140 - Nearest Rank Percentiles (solution)
# Nearest-rank percentiles for latency samples.
import math


def percentile(samples, p):
    if not 0 <= p <= 100:
        raise ValueError("p must be between 0 and 100")
    if not samples:
        raise ValueError("no samples")
    ordered = sorted(samples)
    rank = max(1, math.ceil(p / 100 * len(ordered)))
    return ordered[rank - 1]


def latency_summary(samples):
    return {
        "p50": percentile(samples, 50),
        "p95": percentile(samples, 95),
        "p99": percentile(samples, 99),
        "max": percentile(samples, 100),
    }


def slowest(samples, n):
    ordered = sorted(samples, reverse=True)
    return ordered[:n]
