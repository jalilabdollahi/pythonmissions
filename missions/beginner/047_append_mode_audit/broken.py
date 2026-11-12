# Mission 047 - Audit Trail Overwritten
# Append-only audit trail for scheduler restarts.
import os


def record_action(path, user, action):
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(f"{user} {action}")


def history(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as handle:
        return handle.read().splitlines()
