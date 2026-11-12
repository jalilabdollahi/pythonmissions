# Mission 262 - Checkout Error Spike Detector (solution)
# Rolling z-score detector that flags unusual checkout error counts per minute.
import math
from collections import deque, namedtuple

Anomaly = namedtuple("Anomaly", ["ts", "value", "z"])


class ZScoreDetector:
    def __init__(self, window=20, threshold=3.0, warmup=5):
        if warmup < 2:
            raise ValueError("warmup must be at least 2 for a standard deviation")
        self.values = deque(maxlen=window)
        self.threshold = threshold
        self.warmup = warmup

    def zscore(self, value):
        """How many sample standard deviations `value` is from the baseline."""
        sample = self.values
        n = len(sample)
        mean = sum(sample) / n
        variance = sum((v - mean) ** 2 for v in sample) / (n - 1)
        std = math.sqrt(variance)
        if std == 0:
            if value == mean:
                return 0.0
            return math.copysign(math.inf, value - mean)
        return (value - mean) / std

    def exceeds(self, z):
        return abs(z) > self.threshold

    def observe(self, ts, value):
        """Return an Anomaly, or None when the value looks normal."""
        if len(self.values) < self.warmup:
            self.values.append(value)
            return None
        z = self.zscore(value)
        if self.exceeds(z):
            return Anomaly(ts, value, z)
        self.values.append(value)
        return None


def scan(series, **options):
    """series: iterable of (ts, value). Returns the list of anomalies in order."""
    detector = ZScoreDetector(**options)
    found = []
    for ts, value in series:
        hit = detector.observe(ts, value)
        if hit is not None:
            found.append(hit)
    return found


def group_incidents(anomalies, max_gap=120):
    """Merge anomalies whose timestamps are within `max_gap` seconds of each other."""
    incidents = []
    for hit in sorted(anomalies, key=lambda a: a.ts):
        if incidents and hit.ts - incidents[-1]["end"] <= max_gap:
            incidents[-1]["end"] = hit.ts
            incidents[-1]["count"] += 1
            incidents[-1]["peak"] = max(incidents[-1]["peak"], hit.value)
        else:
            incidents.append({"start": hit.ts, "end": hit.ts, "count": 1, "peak": hit.value})
    return incidents


def describe(anomaly):
    direction = "above" if anomaly.z > 0 else "below"
    return f"t={anomaly.ts}: {anomaly.value} is {abs(anomaly.z):.1f} sigma {direction} baseline"


if __name__ == "__main__":
    demo = [(i * 60, 10 + (i % 3)) for i in range(12)] + [(720, 90)]
    print(scan(demo))
