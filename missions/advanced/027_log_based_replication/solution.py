# Mission 027 (Advanced) - Log-Based Replication
# Fixed solution

class ReplicationLog:
    def __init__(self):
        self._log = []
        self._applied_lsn = 0

    def append(self, lsn, operation, data):
        self._log.append({"lsn": lsn, "op": operation, "data": data})

    def get_entries_after(self, lsn):
        return [e for e in self._log if e["lsn"] > lsn]

class ReplicaApplier:
    def __init__(self):
        self._state = {}
        self._applied_lsn = 0
        self._gaps = []

    def apply_batch(self, entries):
        sorted_entries = sorted(entries, key=lambda e: e["lsn"])
        for entry in sorted_entries:
            expected = self._applied_lsn + 1
            if entry["lsn"] != expected:
                self._gaps.append(expected)
                continue  # skip out-of-order entry
            self._apply_entry(entry)
            self._applied_lsn = entry["lsn"]
        return self._gaps

    def _apply_entry(self, entry):
        if entry["op"] == "set":
            self._state[entry["data"]["key"]] = entry["data"]["value"]
        elif entry["op"] == "del":
            self._state.pop(entry["data"]["key"], None)
