# Mission 137 - Inventory Precedence (solution)
# Resolve host variables: all < groups (in listed order) < host vars.


def resolve_vars(inventory, host):
    entry = inventory["hosts"][host]
    merged = dict(inventory["all"])
    for group in entry.get("groups", []):
        merged.update(inventory["groups"][group])
    merged.update(entry.get("vars", {}))
    return merged


def diff_hosts(inventory, a, b):
    left = resolve_vars(inventory, a)
    right = resolve_vars(inventory, b)
    diff = {}
    for name in sorted(set(left) | set(right)):
        if left.get(name) != right.get(name):
            diff[name] = (left.get(name), right.get(name))
    return diff


def hosts_missing_var(inventory, name):
    return sorted(h for h in inventory["hosts"] if name not in resolve_vars(inventory, h))
