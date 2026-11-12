# Mission 228 - Replica Delta Finder (solution)
# Merkle trees over fixed hash buckets to find which keys differ between replicas.
import hashlib

BUCKETS = 8


def _h(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def bucket_of(key):
    return int(hashlib.md5(key.encode("utf-8")).hexdigest()[:8], 16) % BUCKETS


def leaf_hash(items):
    body = "".join(f"{k}\x1f{v}\x1e" for k, v in sorted(items))
    return _h("leaf:" + body)


def build_tree(store):
    buckets = [[] for _ in range(BUCKETS)]
    for key, value in store.items():
        buckets[bucket_of(key)].append((key, value))
    level = [leaf_hash(items) for items in buckets]
    levels = [level]
    while len(level) > 1:
        level = [_h(level[i] + level[i + 1]) for i in range(0, len(level), 2)]
        levels.append(level)
    return levels


def root_hash(store):
    return build_tree(store)[-1][0]


def diff_buckets(tree_a, tree_b):
    found = []

    def walk(level, index):
        if tree_a[level][index] == tree_b[level][index]:
            return
        if level == 0:
            found.append(index)
            return
        walk(level - 1, index * 2)
        walk(level - 1, index * 2 + 1)

    walk(len(tree_a) - 1, 0)
    return sorted(found)


def diff_keys(a, b):
    buckets = set(diff_buckets(build_tree(a), build_tree(b)))
    keys = set(a) | set(b)
    return sorted(
        k for k in keys if bucket_of(k) in buckets and a.get(k) != b.get(k)
    )


def repair_plan(source, target):
    plan = {"copy": {}, "delete": []}
    for key in diff_keys(source, target):
        if key in source:
            plan["copy"][key] = source[key]
        else:
            plan["delete"].append(key)
    return plan


def apply_plan(target, plan):
    target.update(plan["copy"])
    for key in plan["delete"]:
        target.pop(key, None)
    return target
