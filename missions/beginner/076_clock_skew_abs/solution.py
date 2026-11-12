# Mission 076 - Drifting Clocks Audit (solution)
# Flags hosts whose clocks drift too far from the reference time.


def skew_seconds(host_time, reference_time):
    return host_time - reference_time


def is_skewed(host_time, reference_time, tolerance):
    skew = skew_seconds(host_time, reference_time)
    return abs(skew) > tolerance


def find_skewed_hosts(readings, reference_time, tolerance):
    bad = []
    for name, epoch in readings.items():
        if is_skewed(epoch, reference_time, tolerance):
            bad.append(name)
    return sorted(bad)


def worst_offender(readings, reference_time):
    if not readings:
        return None
    return max(readings, key=lambda n: abs(skew_seconds(readings[n], reference_time)))


def format_report(readings, reference_time, tolerance):
    lines = []
    for name in find_skewed_hosts(readings, reference_time, tolerance):
        lines.append(f"{name}: {skew_seconds(readings[name], reference_time):+d}s")
    return "\n".join(lines) or "all clocks in sync"


if __name__ == "__main__":
    sample = {"db-1": 1_700_000_000, "db-2": 1_699_999_700, "db-3": 1_700_000_090}
    print(format_report(sample, 1_700_000_000, 30))
