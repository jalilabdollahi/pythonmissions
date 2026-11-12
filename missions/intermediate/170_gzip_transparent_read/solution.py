# Mission 170 - Rotated Log Reader (solution)
# Read plain and gzip-compressed logs through one interface.
import gzip

GZIP_MAGIC = b"\x1f\x8b"


def is_gzip(path):
    with open(path, "rb") as handle:
        return handle.read(2) == GZIP_MAGIC


def open_log(path):
    if is_gzip(path):
        return gzip.open(path, "rt", encoding="utf-8")
    return open(path, encoding="utf-8")


def count_levels(paths):
    counts = {}
    for path in paths:
        with open_log(path) as handle:
            for line in handle:
                parts = line.split()
                if len(parts) < 2:
                    continue
                level = parts[1]
                counts[level] = counts.get(level, 0) + 1
    return counts
