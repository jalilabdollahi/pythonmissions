# Mission 170 - Rotated Log Reader
# Read plain and gzip-compressed logs through one interface.
import gzip

GZIP_MAGIC = b"\x1f\x8b"


def is_gzip(path):
    return str(path).endswith(".gz")


def open_log(path):
    if is_gzip(path):
        return gzip.open(path)
    return open(path, encoding="utf-8")


def count_levels(paths):
    counts = {}
    for path in paths:
        with open_log(path) as handle:
            for line in handle:
                level = line.split()[1]
                counts[level] = counts.get(level, 0) + 1
    return counts
