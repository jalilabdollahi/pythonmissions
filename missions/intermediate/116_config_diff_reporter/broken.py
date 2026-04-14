# Mission 116 - Config Diff Reporter
# Fix the 2 bugs in this script.

def config_diff(old, new):
    """Return dict with added, removed, changed keys."""
    old_keys = set(old.keys())
    new_keys = set(new.keys())

    added = {k: new[k] for k in old_keys - new_keys}   # BUG 1: added = new_keys - old_keys
    removed = {k: old[k] for k in new_keys - old_keys}  # BUG 2: removed = old_keys - new_keys

    changed = {}
    for k in old_keys & new_keys:
        if old[k] != new[k]:
            changed[k] = {"old": old[k], "new": new[k]}

    return {"added": added, "removed": removed, "changed": changed}

def format_diff(diff):
    lines = []
    for k, v in diff["added"].items():
        lines.append(f"+ {k}: {v}")
    for k, v in diff["removed"].items():
        lines.append(f"- {k}: {v}")
    for k, v in diff["changed"].items():
        lines.append(f"~ {k}: {v['old']} -> {v['new']}")
    return "\n".join(lines)
