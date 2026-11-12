# Mission 285 - Telemetry Sequence Guard (solution)
# Per-producer sequence tracking that drops duplicates and reports gaps in edge telemetry.


class _Stream:
    def __init__(self):
        self.last = 0
        self.missing = set()


class SequenceTracker:
    """Producers number their messages 1, 2, 3, ... and may be re-sent or reordered."""

    def __init__(self):
        self._streams = {}
        self.counts = {"ok": 0, "gap": 0, "late": 0, "duplicate": 0}

    def accept(self, producer, seq):
        """Classify one message: ok, gap, late (fills a gap) or duplicate."""
        stream = self._streams.setdefault(producer, _Stream())
        status = self._classify(stream, seq)
        self.counts[status] += 1
        return status

    @staticmethod
    def _classify(stream, seq):
        if seq in stream.missing:
            stream.missing.discard(seq)
            return "late"
        if seq <= stream.last:
            return "duplicate"
        status = "ok"
        if seq > stream.last + 1:
            stream.missing.update(range(stream.last + 1, seq))
            status = "gap"
        stream.last = seq
        return status

    def gaps(self, producer):
        stream = self._streams.get(producer)
        return sorted(stream.missing) if stream else []

    def gap_ranges(self, producer):
        """Collapse missing numbers into inclusive (first, last) ranges for alerting."""
        ranges = []
        for seq in self.gaps(producer):
            if ranges and ranges[-1][1] == seq - 1:
                ranges[-1] = (ranges[-1][0], seq)
            else:
                ranges.append((seq, seq))
        return ranges

    def producers(self):
        return sorted(self._streams)

    def highest(self, producer):
        stream = self._streams.get(producer)
        return stream.last if stream else 0

    def is_complete(self, producer):
        return self.highest(producer) > 0 and not self.gaps(producer)


def lossy_producers(tracker):
    """Producers that still have unfilled gaps, with their missing ranges."""
    return {p: tracker.gap_ranges(p) for p in tracker.producers() if tracker.gaps(p)}


def deliver(tracker, messages):
    """Return payloads that should be processed, in arrival order."""
    accepted = []
    for producer, seq, payload in messages:
        if tracker.accept(producer, seq) != "duplicate":
            accepted.append(payload)
    return accepted
