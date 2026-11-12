# Mission 139 - Smoothing Latency
# Trailing moving average and spike detection for latency samples.


def moving_average(values, window):
    if window < 1:
        raise ValueError("window must be at least 1")
    result = []
    for i in range(len(values)):
        start = max(0, i - window)
        chunk = values[start : i + 1]
        result.append(round(sum(chunk) / window, 2))
    return result


def spike_indices(values, window, limit):
    smoothed = moving_average(values, window)
    return [i for i, value in enumerate(smoothed) if value >= limit]


def latest_trend(values, window):
    """Return 'rising', 'falling' or 'flat' by comparing the last two smoothed values."""
    smoothed = moving_average(values, window)
    if len(smoothed) < 2:
        return "flat"
    if smoothed[-1] > smoothed[-2]:
        return "rising"
    if smoothed[-1] < smoothed[-2]:
        return "falling"
    return "flat"
