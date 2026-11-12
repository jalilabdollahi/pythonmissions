# Mission 261 - Tidewater Capacity Crystal Ball (solution)
# Least-squares trend forecasting used to decide how many encoder replicas to pre-warm.
import math


def fit_trend(points):
    """points: list of (unix_seconds, cores_in_use). Returns (slope, intercept)."""
    n = len(points)
    if n < 2:
        raise ValueError("need at least two samples")
    mean_t = sum(t for t, _ in points) / n
    mean_v = sum(v for _, v in points) / n
    sxx = sum((t - mean_t) ** 2 for t, _ in points)
    if sxx == 0:
        raise ValueError("all samples share one timestamp")
    sxy = sum((t - mean_t) * (v - mean_v) for t, v in points)
    slope = sxy / sxx
    intercept = mean_v - slope * mean_t
    return slope, intercept


def recent_window(points, now, span):
    """Samples taken within the last `span` seconds, boundary included."""
    cutoff = now - span
    return sorted(p for p in points if cutoff <= p[0] <= now)


def predict(points, at):
    slope, intercept = fit_trend(points)
    return slope * at + intercept


def seconds_until(points, limit, now):
    """Seconds from `now` until the trend line reaches `limit`.

    Returns 0 if the trend is already at or above the limit and None if the
    trend will never get there.
    """
    slope, intercept = fit_trend(points)
    current = slope * now + intercept
    if current >= limit:
        return 0.0
    if slope <= 0:
        return None
    return (limit - intercept) / slope - now


def replicas_needed(load, per_replica, headroom=0.2, minimum=2):
    """Replicas so that each runs at (1 - headroom) of its capacity at most."""
    usable = per_replica * (1 - headroom)
    wanted = math.ceil(load / usable)
    return max(minimum, wanted)


def fit_quality(points):
    """R squared of the fitted line; 1.0 means the samples are perfectly linear."""
    slope, intercept = fit_trend(points)
    mean_v = sum(v for _, v in points) / len(points)
    total = sum((v - mean_v) ** 2 for _, v in points)
    if total == 0:
        return 1.0
    residual = sum((v - (slope * t + intercept)) ** 2 for t, v in points)
    return 1 - residual / total


def plan(points, now, horizon, per_replica, span=1800):
    window = recent_window(points, now, span)
    expected = predict(window, now + horizon)
    return {
        "samples": len(window),
        "expected_load": round(max(expected, 0.0), 3),
        "replicas": replicas_needed(max(expected, 0.0), per_replica),
    }


if __name__ == "__main__":
    demo = [(0, 8.0), (300, 9.0), (600, 10.5), (900, 11.0)]
    print(plan(demo, 900, 600, 4.0))
