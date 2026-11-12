# Mission 056 - Bytes That Add Up To Nonsense
# Aggregates network cost rows exported as CSV.
import csv


def load(path):
    with open(path, newline="") as handle:
        return list(csv.DictReader(handle))


def bytes_by_service(rows):
    totals = {}
    for row in rows:
        service = row["service"]
        totals[service] = totals.get(service, "") + row["bytes"]
    return totals


def slowest_row(rows):
    return max(rows, key=lambda row: row["latency_ms"])


def busiest_service(rows):
    totals = bytes_by_service(rows)
    return max(totals, key=totals.get)


def report(rows):
    lines = []
    for service, total in sorted(bytes_by_service(rows).items()):
        lines.append("%s: %s bytes" % (service, total))
    return "\n".join(lines)


if __name__ == "__main__":
    import sys

    print(report(load(sys.argv[1])))
