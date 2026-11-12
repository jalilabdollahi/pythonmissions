# Mission 282 - NDJSON Firehose (solution)
# Stream a huge newline-delimited JSON export lazily, skipping and counting bad lines.
import json
from collections import Counter


def new_stats():
    return {"lines": 0, "records": 0, "blank": 0, "malformed": 0, "bad_line_numbers": []}


def _reject(stats, lineno):
    stats["malformed"] += 1
    stats["bad_line_numbers"].append(lineno)


def iter_records(lines, stats):
    """Yield one dict per valid line. Line numbers in stats are 1-based."""
    for lineno, raw in enumerate(lines, start=1):
        stats["lines"] += 1
        text = raw.strip()
        if not text:
            stats["blank"] += 1
            continue
        try:
            record = json.loads(text)
        except ValueError:
            _reject(stats, lineno)
            continue
        if not isinstance(record, dict):
            _reject(stats, lineno)
            continue
        stats["records"] += 1
        yield record


def read_file(path):
    """Open an export and yield its raw lines one at a time."""
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            yield line


def batched(items, size):
    batch = []
    for item in items:
        batch.append(item)
        if len(batch) == size:
            yield batch
            batch = []
    if batch:
        yield batch


def count_by(records, field):
    counts = Counter()
    for record in records:
        counts[record.get(field, "unknown")] += 1
    return dict(counts)


def summarize(path, field):
    stats = new_stats()
    counts = count_by(iter_records(read_file(path), stats), field)
    return counts, stats


if __name__ == "__main__":
    import sys

    print(summarize(sys.argv[1], "level"))
