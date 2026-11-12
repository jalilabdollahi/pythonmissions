# Mission 240 - Log-Structured Compactor
# Minimal LSM tree: memtable flush, newest-wins merge, tombstone-aware compaction.
import heapq

TOMBSTONE = object()


def _tag(run, age):
    for key, value in run:
        yield key, age, value


def merge_runs(runs, last_level):
    streams = [_tag(run, age) for age, run in enumerate(runs)]
    merged = []
    previous_key = None
    first = True
    for key, _age, value in heapq.merge(*streams, key=lambda item: (item[0], -item[1])):
        if not first and key == previous_key:
            continue
        first = False
        previous_key = key
        if value is TOMBSTONE:
            continue
        merged.append((key, value))
    return merged


def get_from_runs(runs, key):
    for run in runs:
        for run_key, value in run:
            if run_key == key:
                if value is TOMBSTONE:
                    break
                return value
    return None


class LsmTree:
    def __init__(self, level0_limit=2):
        self.memtable = {}
        self.level0 = []
        self.level1 = []
        self.level0_limit = level0_limit

    def put(self, key, value):
        self.memtable[key] = value

    def delete(self, key):
        self.memtable[key] = TOMBSTONE

    def flush(self):
        if not self.memtable:
            return
        self.level0.insert(0, sorted(self.memtable.items()))
        self.memtable = {}
        if len(self.level0) >= self.level0_limit:
            self.compact()

    def compact(self):
        runs = list(self.level0) + ([self.level1] if self.level1 else [])
        self.level1 = merge_runs(runs, last_level=False)
        self.level0 = []

    def get(self, key):
        if key in self.memtable:
            value = self.memtable[key]
            return None if value is TOMBSTONE else value
        return get_from_runs(self.level0 + [self.level1], key)

    def items(self):
        view = {}
        for run in reversed(self.level0 + [self.level1]):
            for key, value in run:
                view[key] = value
        return sorted((k, v) for k, v in view.items() if v is not TOMBSTONE)
