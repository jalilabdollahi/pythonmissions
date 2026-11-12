# Mission 299 - Config Merge (solution)
# Three-way merge of nested configuration dicts with conflict detection.
import copy

MISSING = object()


class MergeConflict(Exception):
    def __init__(self, paths):
        super().__init__("conflicts at: " + ", ".join(paths))
        self.paths = paths


def _copy(value):
    return value if value is MISSING else copy.deepcopy(value)


def three_way_merge(base, ours, theirs):
    """Merge two edited copies of `base`. Returns (merged, conflict_paths).

    A side that did not change a key defers to the other side; if both changed it to the same
    value that value wins; if both changed it differently the key is a conflict (ours is kept
    in the output) unless both values are dicts, which are merged key by key.
    """
    conflicts = []
    merged = _merge_dicts(base, ours, theirs, "", conflicts)
    return merged, conflicts


def _merge_dicts(base, ours, theirs, prefix, conflicts):
    merged = {}
    for key in sorted(set(base) | set(ours) | set(theirs)):
        path = f"{prefix}.{key}" if prefix else key
        value = _resolve(
            base.get(key, MISSING), ours.get(key, MISSING), theirs.get(key, MISSING), path, conflicts
        )
        if value is not MISSING:
            merged[key] = value
    return merged


def _resolve(b, o, t, path, conflicts):
    if o == t:
        return _copy(o)
    if o == b:
        return _copy(t)
    if t == b:
        return _copy(o)
    if isinstance(o, dict) and isinstance(t, dict):
        return _merge_dicts(b if isinstance(b, dict) else {}, o, t, path, conflicts)
    conflicts.append(path)
    return _copy(o)


def merge_strict(base, ours, theirs):
    merged, conflicts = three_way_merge(base, ours, theirs)
    if conflicts:
        raise MergeConflict(conflicts)
    return merged


def changed_paths(base, new, prefix=""):
    """Dotted paths whose value differs between base and new (for review summaries)."""
    paths = []
    for key in sorted(set(base) | set(new)):
        path = f"{prefix}.{key}" if prefix else key
        b, n = base.get(key, MISSING), new.get(key, MISSING)
        if isinstance(b, dict) and isinstance(n, dict):
            paths.extend(changed_paths(b, n, path))
        elif b != n:
            paths.append(path)
    return paths
