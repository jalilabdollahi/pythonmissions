# Mission 028 (Advanced) - Adaptive Timeout
# Fix the 2 bugs in this script.
import statistics

class AdaptiveTimeout:
    def __init__(self, alpha=0.1, multiplier=2.0, min_timeout=0.1, max_timeout=30.0):
        self.alpha = alpha
        self.multiplier = multiplier
        self.min_timeout = min_timeout
        self.max_timeout = max_timeout
        self._ewma = None
        self._samples = []

    def record_latency(self, latency_s):
        self._samples.append(latency_s)
        if len(self._samples) > 100:
            self._samples.pop(0)
        if self._ewma is None:
            self._ewma = latency_s
        else:
            self._ewma = self.alpha * self._ewma + (1 - self.alpha) * latency_s  # BUG 1: order inverted

    def get_timeout(self):
        if not self._samples:
            return self.max_timeout
        p99 = statistics.quantiles(self._samples, n=10)[-1]  # BUG 2: n=10 gives deciles (p90), not p99
        timeout = p99 * self.multiplier
        return max(self.min_timeout, min(self.max_timeout, timeout))
