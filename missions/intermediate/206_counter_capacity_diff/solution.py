# Mission 206 - Fleet Capacity Diff (solution)
# Compare current and planned instance counts using collections.Counter.
import math
from collections import Counter


def capacity_diff(have, want):
    net = Counter(have)
    net.subtract(want)
    to_add = {kind: -count for kind, count in net.items() if count < 0}
    to_remove = {kind: count for kind, count in net.items() if count > 0}
    return to_add, to_remove


def total_instances(counter):
    return sum(counter.values())


def with_headroom(want, pct):
    return Counter({kind: math.ceil(count * (1 + pct / 100)) for kind, count in want.items()})


def biggest_surplus(have, want, n=1):
    _, to_remove = capacity_diff(have, want)
    return Counter(to_remove).most_common(n)


def utilisation(have, want):
    needed = total_instances(want)
    return round(needed / total_instances(have), 2) if have else 0.0


def plan_summary(have, want):
    to_add, to_remove = capacity_diff(have, want)
    lines = []
    for kind in sorted(to_add):
        lines.append(f"add {to_add[kind]} x {kind}")
    for kind in sorted(to_remove):
        lines.append(f"remove {to_remove[kind]} x {kind}")
    return lines or ["no changes"]


if __name__ == "__main__":
    now = Counter({"m5.large": 4, "c5.xlarge": 2})
    plan = Counter({"m5.large": 6, "r5.large": 1})
    print("\n".join(plan_summary(now, plan)))
