# Mission 267 - Parcel Request Timeline
# Stitch log lines from several services into one ordered timeline per request id.


def normalize_id(raw):
    """Request ids arrive with inconsistent case and stray whitespace."""
    if raw is None:
        return None
    cleaned = raw
    return cleaned or None


def adjust(entry, skew):
    """Return a copy of the entry whose ts is corrected by its service's clock skew.

    skew[service] is how many seconds that service's clock runs AHEAD of true time.
    """
    fixed = dict(entry)
    fixed["ts"] = entry["ts"] + skew.get(entry["service"], 0.0)
    return fixed


def correlate(entries, skew=None):
    """Group entries by request id. Returns (timelines, unattributed_count)."""
    skew = skew or {}
    timelines = {}
    unattributed = 0
    for entry in entries:
        rid = normalize_id(entry.get("request_id"))
        if rid is None:
            unattributed += 1
            continue
        timelines.setdefault(rid, []).append(adjust(entry, skew))
    for rid in timelines:
        timelines[rid].sort(key=lambda e: e["ts"])
    return timelines, unattributed


def hops(timeline):
    """Number of times the request moved from one service to another."""
    count = 0
    for before, after in zip(timeline, timeline[1:]):
        if before["service"] != after["service"]:
            count += 1
    return len({e["service"] for e in timeline}) - 1


def summarize(timeline):
    return {
        "services": sorted({e["service"] for e in timeline}),
        "hops": hops(timeline),
        "duration": round(timeline[-1]["ts"] - timeline[0]["ts"], 6),
        "errors": sum(1 for e in timeline if e.get("level") == "ERROR"),
    }


def slowest_gap(timeline):
    """(gap_seconds, from_service, to_service) of the longest wait between lines."""
    best = (0.0, None, None)
    for before, after in zip(timeline, timeline[1:]):
        gap = after["ts"] - before["ts"]
        if gap > best[0]:
            best = (round(gap, 6), before["service"], after["service"])
    return best


def failing_requests(timelines):
    return sorted(rid for rid, lines in timelines.items() if any(e.get("level") == "ERROR" for e in lines))


if __name__ == "__main__":
    sample = [
        {"ts": 10.0, "service": "edge", "seq": 1, "request_id": "R1", "msg": "in"},
        {"ts": 10.2, "service": "router", "seq": 1, "request_id": "r1", "msg": "route"},
    ]
    lines, _ = correlate(sample)
    print(summarize(lines["r1"]))
