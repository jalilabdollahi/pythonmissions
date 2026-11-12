# Mission 144 - Honest Uptime
# Compute downtime and uptime percentage from possibly overlapping outages.


def downtime_minutes(windows, period_start, period_end):
    events = []
    total = 0
    for start, end in windows:
        start = start
        end = end
        if end <= start:
            continue
        total += end - start
    return total


def uptime_percent(windows, period_start, period_end):
    length = period_end - period_start
    if length <= 0:
        raise ValueError("empty reporting period")
    down = downtime_minutes(windows, period_start, period_end)
    return round(100 * down / length, 3)


def worst_outage(windows):
    if not windows:
        return None
    return max(windows, key=lambda w: w[1] - w[0])
