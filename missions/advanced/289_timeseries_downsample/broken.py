# Mission 289 - Metric Rollup
# Downsample raw (timestamp, value) points into epoch-aligned buckets, keeping gaps visible.

AGGREGATORS = {
    "avg": lambda values: sum(values) // len(values),
    "sum": sum,
    "max": max,
    "min": min,
    "last": lambda values: values[-1],
}


def bucket_start(ts, step):
    """Buckets are aligned to the epoch, not to the first sample we happen to see."""
    return round(ts / step) * step


def downsample(points, step, agg="avg", start=None, end=None):
    """Return [(bucket_ts, value_or_None)] for every bucket in [start, end).

    A bucket with no samples is reported as None so charts show a gap instead of
    silently joining the neighbours. Input may arrive unsorted.
    """
    if step <= 0:
        raise ValueError("step must be positive")
    func = AGGREGATORS[agg]
    ordered = list(points)
    if start is not None:
        ordered = [p for p in ordered if p[0] >= start]
    if end is not None:
        ordered = [p for p in ordered if p[0] < end]
    if not ordered:
        return []
    grouped = {}
    for ts, value in ordered:
        grouped.setdefault(bucket_start(ts, step), []).append(value)
    first = bucket_start(start if start is not None else ordered[0][0], step)
    stop = end if end is not None else bucket_start(ordered[-1][0], step) + step
    out = []
    t = first
    while t < stop:
        values = grouped.get(t)
        if values:
            out.append((t, func(values)))
        t += step
    return out


def gap_count(series):
    return sum(1 for _, value in series if value is None)


def coverage(series):
    """Fraction of buckets that actually hold data."""
    if not series:
        return 0.0
    return 1 - gap_count(series) / len(series)


def fill_forward(series, max_gap=1):
    """Repeat the last known value over at most `max_gap` consecutive empty buckets."""
    out = []
    last, run = None, 0
    for ts, value in series:
        if value is None:
            run += 1
            out.append((ts, last if last is not None and run <= max_gap else None))
        else:
            last, run = value, 0
            out.append((ts, value))
    return out
