# Mission 166 - Stale Artifacts Sweep
# List files that have not been modified for more than N days.
import os

SECONDS_PER_DAY = 86400


def find_old_files(root, days, now):
    cutoff = now - days * 3600
    found = []
    for entry in os.scandir(root):
        if entry.stat().st_mtime > cutoff:
            found.append(entry.name)
    return sorted(found)


def total_size(root, names):
    return sum(os.path.getsize(os.path.join(root, name)) for name in names)
