# Mission 173 - Spot The Drift
# Compare two flat config dicts and report added, removed and changed keys.
def diff_configs(old, new):
    added = {k: new[k] for k in new if not old.get(k)}
    removed = {k: old[k] for k in old if k not in new}
    changed = {k: (old[k], new[k]) for k in old if k in new and old[k] is not new[k]}
    return {"added": added, "removed": removed, "changed": changed}


def is_clean(diff):
    return not (diff["added"] or diff["removed"] or diff["changed"])


def summarize(diff):
    lines = []
    for key in sorted(diff["added"]):
        lines.append("+ %s=%s" % (key, diff["added"][key]))
    for key in diff["removed"]:
        lines.append("- %s=%s" % (key, diff["removed"][key]))
    for key in sorted(diff["changed"]):
        before, after = diff["changed"][key]
        lines.append("~ %s: %s -> %s" % (key, before, after))
    return "\n".join(lines) if lines else "no differences"


def main():
    old = {"workers": 2, "debug": False, "region": "eu"}
    new = {"workers": 4, "debug": False, "zone": "b"}
    diff = diff_configs(old, new)
    print(summarize(diff))
    print("clean" if is_clean(diff) else "drift detected")


if __name__ == "__main__":
    main()
