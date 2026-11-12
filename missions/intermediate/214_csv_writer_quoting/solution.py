# Mission 214 - Audit CSV Export (solution)
# Export host audit results to CSV and read them back.
import csv
from collections import Counter

FIELDS = ["host", "status", "note"]


def write_report(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(FIELDS)
        for row in rows:
            writer.writerow([row[name] for name in FIELDS])


def append_row(path, row):
    with open(path, "a", newline="", encoding="utf-8") as handle:
        csv.writer(handle).writerow([row[name] for name in FIELDS])


def read_report(path):
    with open(path, "r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def status_counts(path):
    return dict(Counter(row["status"] for row in read_report(path)))


def notes_for(path, status):
    return [row["note"] for row in read_report(path) if row["status"] == status]


def failing_hosts(path):
    return sorted(row["host"] for row in read_report(path) if row["status"] != "pass")


if __name__ == "__main__":
    write_report("audit.csv", [{"host": "db1", "status": "warn", "note": "disk 91%, rotating"}])
    print(read_report("audit.csv"))
