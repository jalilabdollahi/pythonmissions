# Mission 121 - Edge Log Decoder
# Parse nginx access log lines (common and combined formats) into dicts.
import re

LINE_RE = re.compile(
    r'^(?P<ip>\S+) \S+ (?P<user>\S+) '
    r'\[(?P<time>[^\]]+)\] '
    r'"(?P<method>[A-Z]+) (?P<path>\S+) (?P<proto>[^"]+)" '
    r'(?P<status>\d{3}) (?P<bytes>\d+)'
    r' "(?P<referer>[^"]*)" "(?P<agent>.*)"(?: "(?P<xff>[^"]*)")?$'
)


def parse_line(line):
    match = LINE_RE.match(line.strip())
    if match is None:
        return None
    record = match.groupdict()
    record["status"] = int(record["status"])
    record["bytes"] = int(record["bytes"])
    return record


def parse_lines(lines):
    records = []
    bad = 0
    for line in lines:
        if not line.strip():
            continue
        record = parse_line(line)
        if record is None:
            bad += 1
        else:
            records.append(record)
    return records, bad


def total_bytes(records):
    return sum(r["bytes"] for r in records)


if __name__ == "__main__":
    import sys

    recs, bad = parse_lines(sys.stdin)
    print(f"{len(recs)} ok, {bad} bad, {total_bytes(recs)} bytes")
