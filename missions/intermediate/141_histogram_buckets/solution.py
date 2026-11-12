# Mission 141 - Cumulative Buckets (solution)
# A Prometheus-style latency histogram with cumulative "le" buckets.


class LatencyHistogram:
    def __init__(self, bounds):
        self.bounds = sorted(bounds)
        self._buckets = {bound: 0 for bound in self.bounds}
        self.count = 0
        self.total = 0.0

    def observe(self, seconds):
        self.count += 1
        self.total += seconds
        for bound in self.bounds:
            if seconds <= bound:
                self._buckets[bound] += 1
                

    def snapshot(self):
        result = {str(bound): self._buckets[bound] for bound in self.bounds}
        result["+Inf"] = self.count
        return result

    def mean(self):
        return self.total / self.count if self.count else 0.0


def render_buckets(name, histogram):
    lines = [f'{name}_bucket{{le="{label}"}} {value}' for label, value in histogram.snapshot().items()]
    lines.append(f"{name}_sum {histogram.total}")
    lines.append(f"{name}_count {histogram.count}")
    return lines
