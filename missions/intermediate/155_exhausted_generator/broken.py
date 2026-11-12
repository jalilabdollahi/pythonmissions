# Mission 155 - Used-Up Iterators
# Summaries over log data that may arrive as one-shot iterators.


def parse_ms(lines):
    return (int(line.rsplit(" ", 1)[1]) for line in lines if line.strip())


def latency_summary(lines):
    values = parse_ms(lines)
    count = sum(1 for _ in values)
    if count == 0:
        return {"count": 0, "min": None, "max": None}
    return {"count": count, "min": min(values), "max": max(values)}


def error_report(path):
    with open(path) as handle:
        total = sum(1 for _ in handle)
        errors = [line.strip() for line in handle if "ERROR" in line]
    return total, errors


def recent_failures(events):
    failed = filter(lambda event: event["ok"] is False, events)
    if not any(failed):
        return []
    return list(failed)
