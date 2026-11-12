# Mission 055 - Header Row Counted As Host (solution)
# Summarises per-host request counts from a nightly CSV export.
import csv


def load_rows(path):
    with open(path, newline="") as handle:
        reader = csv.reader(handle)
        next(reader, None)
        return [row for row in reader]


def host_count(path):
    return len(load_rows(path))


def total_requests(path):
    return sum(int(row[1]) for row in load_rows(path))


def busiest_host(path):
    rows = load_rows(path)
    best = max(rows, key=lambda row: int(row[1]))
    return best[0]


def average_requests(path):
    return total_requests(path) / host_count(path)


if __name__ == "__main__":
    import sys

    print(total_requests(sys.argv[1]))
