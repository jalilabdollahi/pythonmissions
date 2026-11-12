# Mission 079 - Counting the Errors (solution)
# Summarises request records for the payments dashboard.


def count_errors(records):
    return sum(1 for r in records if r["status"] >= 500)


def error_bytes(records):
    return sum(r["bytes"] for r in records if r["status"] >= 500)


def error_rate(records):
    if not records:
        return 0.0
    return count_errors(records) / len(records)


def count_slow(records, ms_limit):
    return sum(1 for r in records if r.get("ms", 0) > ms_limit)


def render(records):
    rate = error_rate(records) * 100
    return f"{count_errors(records)}/{len(records)} errors ({rate:.1f}%)"


if __name__ == "__main__":
    demo = [
        {"status": 200, "bytes": 512, "ms": 40},
        {"status": 503, "bytes": 90, "ms": 900},
        {"status": 500, "bytes": 10, "ms": 20},
    ]
    print(render(demo))
