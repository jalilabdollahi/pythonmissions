# Mission 171 - Glob Into The Depths (solution)
# Find log and manifest files anywhere under a service tree.
import glob
import os
from collections import Counter
from pathlib import Path


def _rel(path, root):
    return os.path.relpath(path, root).replace(os.sep, "/")


def find_logs(root):
    pattern = os.path.join(root, "**", "*.log")
    return sorted(_rel(p, root) for p in glob.glob(pattern, recursive=True))


def find_manifests(root):
    found = [p for p in Path(root).rglob("*.yaml") if p.is_file()]
    return sorted(_rel(str(p), root) for p in found)


def logs_per_service(root):
    counts = Counter()
    for rel in find_logs(root):
        parts = rel.split("/")
        counts[parts[0] if len(parts) > 1 else "(root)"] += 1
    return dict(counts)


def main(argv=None):
    import sys

    args = sys.argv[1:] if argv is None else argv
    root = args[0] if args else "."
    for rel in find_logs(root):
        print("log      ", rel)
    for rel in find_manifests(root):
        print("manifest ", rel)
    for service, count in sorted(logs_per_service(root).items()):
        print("%-12s %d" % (service, count))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
