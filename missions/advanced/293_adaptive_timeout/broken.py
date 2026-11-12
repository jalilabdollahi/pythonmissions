# Mission 293 - Adaptive Timeout
# Derive request timeouts from the recent p99 latency, clamped between a floor and a ceiling.
import math
from collections import deque


class AdaptiveTimeout:
    def __init__(self, window=50, floor=0.05, ceiling=5.0, multiplier=1.5,
                 min_samples=10, default=1.0, quantile=0.99):
        self.samples = deque()
        self.floor = floor
        self.ceiling = ceiling
        self.multiplier = multiplier
        self.min_samples = min_samples
        self.default = default
        self.quantile = quantile
        self.timeouts = 0

    def record(self, latency):
        """Record the latency of a request that completed."""
        self.samples.append(latency)

    def record_timeout(self, limit):
        """A request that hit the limit took AT LEAST that long, so record the limit itself."""
        self.timeouts += 1

    def percentile(self, q):
        """Nearest-rank percentile of the current window."""
        ordered = sorted(self.samples)
        return ordered[min(int(q * len(ordered)), len(ordered) - 1)]

    def current(self):
        if len(self.samples) < self.min_samples:
            return self.default
        raw = min(self.ceiling, max(self.floor, self.percentile(self.quantile)))
        return raw * self.multiplier

    def settle(self, latency):
        """Apply the current timeout to a request that really needed `latency` seconds.

        Returns True when the request timed out.
        """
        limit = self.current()
        if latency >= limit:
            self.record_timeout(limit)
            return True
        self.record(latency)
        return False

    def snapshot(self):
        return {
            "timeout": self.current(),
            "samples": len(self.samples),
            "timeouts": self.timeouts,
        }


def warm_up(timeout, latencies):
    """Feed a batch of observed latencies and return the resulting timeout."""
    for latency in latencies:
        timeout.record(latency)
    return timeout.current()


if __name__ == "__main__":
    t = AdaptiveTimeout()
    print(warm_up(t, [0.12, 0.09, 0.31] * 10))
    print(t.snapshot())
