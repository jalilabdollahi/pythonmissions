# Mission 174 - Drift Report Printer
# Render unified diffs between deployed and desired config files.
import difflib


def unified(deployed, desired, name):
    diff = difflib.unified_diff(
        desired.splitlines(),
        deployed.splitlines(),
        fromfile="%s.deployed" % name,
        tofile="%s.desired" % name,
    )
    return "\n".join(diff)


def count_changes(diff_text):
    added = removed = 0
    for line in diff_text.splitlines():
        if line.startswith("+"):
            added += 1
        elif line.startswith("-") and not line.startswith("---"):
            removed += 1
    return added, removed


def drift_report(files):
    chunks = []
    for name in sorted(files):
        deployed, desired = files[name]
        if deployed != desired:
            chunks.append(unified(deployed, desired, name))
    return "\n\n".join(chunks) if chunks else "no drift"


def main():
    files = {
        "nginx.conf": ("worker_processes 2;", "worker_processes 4;"),
        "app.env": ("MODE=prod", "MODE=prod"),
    }
    report = drift_report(files)
    print(report)
    print(count_changes(report))


if __name__ == "__main__":
    main()
