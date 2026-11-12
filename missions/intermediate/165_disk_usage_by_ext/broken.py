# Mission 165 - Space Hogs by Extension
# Total file sizes per extension under a directory tree.
import os


def usage_by_extension(top):
    totals = {}
    for dirpath, _dirnames, filenames in os.walk(top):
        for name in filenames:
            size = os.path.getsize(os.path.join(top, name))
            ext = os.path.splitext(name)[1]
            totals[ext] = totals.get(ext, 0) + size
    return totals


def top_extensions(totals, n=3):
    ranked = sorted(totals.items(), key=lambda item: (-item[1], item[0]))
    return ranked[:n]
