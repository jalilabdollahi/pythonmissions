# Mission 263 - Harborlight Latency Smoother
# Time-aware exponentially weighted moving average of request latency per CDN route.
import math


class LatencyEWMA:
    """EWMA whose memory is defined by a half-life in seconds, not a fixed alpha."""

    def __init__(self, half_life=30.0):
        if half_life <= 0:
            raise ValueError("half_life must be positive")
        self.half_life = half_life
        self.value = None
        self.last_ts = None
        self.samples = 0
        self.rejected = 0

    def update(self, latency_ms, ts):
        if latency_ms < 0:
            self.rejected += 1
            return self.value
        if self.value is None:
            self.value = 0.5 * latency_ms
        else:
            dt = ts - self.last_ts
            keep = 0.5 ** (dt / self.half_life)
            self.value = (1 - keep) * self.value + keep * latency_ms
        self.last_ts = ts if self.last_ts is None else max(ts, self.last_ts)
        self.samples += 1
        return self.value


class RouteBoard:
    """One independent tracker per route, plus a degradation check."""

    def __init__(self, half_life=30.0, slow_factor=1.5):
        self.half_life = half_life
        self.slow_factor = slow_factor
        self.fast = {}
        self.baseline = {}

    def record(self, route, latency_ms, ts):
        if route not in self.fast:
            self.fast[route] = LatencyEWMA(self.half_life)
            self.baseline[route] = LatencyEWMA(self.half_life * 20)
        self.fast[route].update(latency_ms, ts)
        self.baseline[route].update(latency_ms, ts)

    def degraded(self, route):
        fast = self.fast[route].value
        slow = self.baseline[route].value
        if fast is None or slow is None:
            return False
        return fast > slow * self.slow_factor

    def report(self):
        rows = []
        for route in sorted(self.fast):
            rows.append(
                {
                    "route": route,
                    "ewma_ms": round(self.fast[route].value, 2),
                    "samples": self.fast[route].samples,
                    "degraded": self.degraded(route),
                }
            )
        return rows


def half_life_for_alpha(alpha, interval):
    """Half-life that matches a classic fixed alpha at a fixed sampling interval."""
    if not 0 < alpha < 1:
        raise ValueError("alpha must be between 0 and 1 exclusive")
    return interval * math.log(0.5) / math.log(1 - alpha)


if __name__ == "__main__":
    board = RouteBoard()
    for i, ms in enumerate([120, 125, 118, 400, 410]):
        board.record("/video", ms, i * 10)
    print(board.report())
