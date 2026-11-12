# Mission 155 - Used-Up Iterators (solution)
# Summaries over log data that may arrive as one-shot iterators.


def parse_ms(lines):
    return (int(line.rsplit(" ", 1)[1]) for line in lines if line.strip())


def latency_summary(lines):
    values = list(parse_ms(lines))
    count = len(values)
    if count == 0:
        return {"count": 0, "min": None, "max": None}
    return {"count": count, "min": min(values), "max": max(values)}


def error_report(path):
    with open(path) as handle:
        lines = handle.read().splitlines()
    total = len(lines)
    errors = [line.strip() for line in lines if "ERROR" in line]
    return total, errors


def recent_failures(events):
    failed = list(filter(lambda event: event["ok"] is False, events))
    if not any(failed):
        return []
    return list(failed)
