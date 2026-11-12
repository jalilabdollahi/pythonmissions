# Mission 157 - Split Groups (solution)
# Per-service latency totals and failing-streak detection built on itertools.groupby.
from itertools import groupby


def per_service_totals(events):
    ordered = sorted(events, key=lambda e: e["service"])
    groups = {}
    for service, group in groupby(ordered, key=lambda e: e["service"]):
        groups[service] = list(group)
    return {
        service: {
            "count": len(items := list(group)),
            "total_ms": sum(e["ms"] for e in items),
        }
        for service, group in groups.items()
    }


def longest_failing_streak(checks):
    streaks = [len(list(run)) for healthy, run in groupby(checks) if not healthy]
    return max(streaks, default=0)
