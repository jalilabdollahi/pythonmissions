# Mission 238 - Deploy Board Projection (solution)
# CQRS read model: a deploy dashboard projected from an unreliable event stream.


class DeployBoard:
    def __init__(self):
        self._reset()

    def _reset(self):
        self.view = {}
        self.versions = {}
        self.pending = {}
        self.duplicates = 0

    def handle(self, event):
        stream = event["stream"]
        version = event["version"]
        last = self.versions.get(stream, 0)
        if version <= last:
            self.duplicates += 1
            return "duplicate"
        if version > last + 1:
            self.pending.setdefault(stream, {})[version] = event
            return "buffered"
        self._apply(event)
        self._drain(stream)
        return "applied"

    def _drain(self, stream):
        buffered = self.pending.get(stream, {})
        while self.versions[stream] + 1 in buffered:
            self._apply(buffered.pop(self.versions[stream] + 1))
        if not buffered:
            self.pending.pop(stream, None)

    def _apply(self, event):
        stream = event["stream"]
        row = self.view.setdefault(
            stream, {"status": "unknown", "release": None, "failures": 0}
        )
        kind = event["type"]
        if kind == "deploy_started":
            row.update(status="deploying", release=event["release"])
        elif kind == "deploy_succeeded":
            row.update(status="healthy", release=event["release"])
        elif kind == "deploy_failed":
            row.update(status="failed")
            row["failures"] += 1
        elif kind == "service_retired":
            row.update(status="retired")
        self.versions[stream] = event["version"]

    def rebuild(self, events):
        self._reset()
        for event in events:
            self.handle(event)
        return self.view

    def status_of(self, stream):
        row = self.view.get(stream)
        return row["status"] if row else None

    def buffered_count(self):
        return sum(len(b) for b in self.pending.values())

    def summary(self):
        counts = {}
        for row in self.view.values():
            counts[row["status"]] = counts.get(row["status"], 0) + 1
        return dict(sorted(counts.items()))

    def releases(self):
        return {s: row["release"] for s, row in sorted(self.view.items()) if row["release"]}

    def failing(self):
        return sorted(s for s, row in self.view.items() if row["status"] == "failed")
