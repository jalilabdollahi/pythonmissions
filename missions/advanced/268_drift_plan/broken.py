# Mission 268 - Kestrel Drift Planner
# Compare declared infrastructure with what is actually running and produce a change plan.

OWNER = "kestrel"
IMMUTABLE = {"region", "engine", "zone"}
COMPUTED = {"id", "arn", "created_at", "status"}
OP_ORDER = ["create", "update", "replace", "delete"]


def normalize(value):
    """Make property values comparable: lists are sets of values, dicts are recursive."""
    if isinstance(value, dict):
        return {k: normalize(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [normalize(v) for v in value]
    return value


def diff_props(want, have):
    """Return {key: (actual, declared)} for every meaningful difference."""
    changes = {}
    for key in sorted(set(want) | set(have)):
        declared = normalize(want.get(key))
        actual = normalize(have.get(key))
        if declared != actual:
            changes[key] = (actual, declared)
    return changes


def is_managed(resource):
    return resource.get("managed_by") == OWNER


def plan(desired, actual):
    """desired/actual: name -> {"type": str, "props": dict, "managed_by": str (actual only)}."""
    actions = []
    for name, want in desired.items():
        have = actual.get(name)
        if have is None:
            actions.append({"op": "create", "name": name, "changes": {}})
            continue
        changes = diff_props(want["props"], have["props"])
        if want["type"] != have["type"]:
            changes["type"] = (have["type"], want["type"])
        if not changes:
            continue
        needs_replace = want["type"] != have["type"]
        actions.append({"op": "replace" if needs_replace else "update", "name": name, "changes": changes})
    for name, have in actual.items():
        if name not in desired:
            actions.append({"op": "delete", "name": name, "changes": {}})
    actions.sort(key=lambda a: (OP_ORDER.index(a["op"]), a["name"]))
    return actions


def summary(actions):
    counts = {op: 0 for op in OP_ORDER}
    for action in actions:
        counts[action["op"]] += 1
    return (
        f"Plan: {counts['create']} to add, {counts['update']} to change, "
        f"{counts['replace']} to replace, {counts['delete']} to destroy."
    )


def has_drift(desired, actual):
    return bool(plan(desired, actual))


def describe(action):
    lines = [f"{action['op']:<8} {action['name']}"]
    for key, (old, new) in sorted(action["changes"].items()):
        lines.append(f"           {key}: {old!r} -> {new!r}")
    return "\n".join(lines)


if __name__ == "__main__":
    want = {"db": {"type": "database", "props": {"size": "large", "region": "eu"}}}
    have = {"db": {"type": "database", "props": {"size": "small", "region": "eu", "id": "x"}, "managed_by": OWNER}}
    print(summary(plan(want, have)))
