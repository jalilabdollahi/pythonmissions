# Mission 208 - Policy Layer Merge
# Build runtime policies from layered dicts with functools.reduce.
import copy
from functools import reduce


def _merge_into(target, source):
    for key, value in source.items():
        if isinstance(value, dict) and isinstance(target.get(key), dict):
            target[key].update(value)
        else:
            target[key] = value
    return target


def merge_layers(*layers):
    return reduce(_merge_into, layers)


def build_store_policy(company, region, store):
    return merge_layers(company, region, store)


def flatten(policy, prefix=""):
    lines = []
    for key in sorted(policy):
        value = policy[key]
        path = f"{prefix}{key}"
        if isinstance(value, dict):
            lines.extend(flatten(value, path + "."))
        else:
            lines.append(f"{path}={value}")
    return lines


def effective_limit(policy, *path, default=None):
    node = policy
    for part in path:
        if not isinstance(node, dict) or part not in node:
            return default
        node = node[part]
    return node


if __name__ == "__main__":
    base = {"checkout": {"timeout": 30, "retries": {"max": 3}}}
    print(build_store_policy(base, {"checkout": {"timeout": 45}}, {}))
