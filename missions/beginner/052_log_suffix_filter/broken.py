# Mission 052 - The Catalog That Vanished
# Finds and removes rotated log files from a directory.
from pathlib import Path


def find_logs(directory):
    names = []
    for entry in Path(directory).iterdir():
        if entry.is_file() and entry.name.endswith("log"):
            names.append(entry.name)
    return sorted(names)


def total_log_bytes(directory):
    base = Path(directory)
    return sum((base / name).stat().st_size for name in find_logs(directory))


def delete_logs(directory):
    base = Path(directory)
    removed = 0
    for name in find_logs(directory):
        (base / name).unlink()
        removed += 1
    return removed


if __name__ == "__main__":
    import sys

    target = sys.argv[1] if len(sys.argv) > 1 else "."
    print("would remove", find_logs(target))
