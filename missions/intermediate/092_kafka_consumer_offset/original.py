# Mission 092 - Kafka Consumer Offset Tracker
# Fix the 2 bugs in this script.

class OffsetTracker:
    def __init__(self):
        self._committed = {}  # partition -> offset
        self._pending = {}

    def record(self, partition, offset):
        """Record that a message was received (not yet processed)."""
        current = self._pending.get(partition, -1)
        if offset > current:
            self._pending[partition] = offset

    def commit(self, partition):
        """Commit the highest pending offset for a partition."""
        if partition in self._pending:
            self._committed[partition] = self._pending[partition]
            del self._pending[partition]

    def process_message(self, partition, offset, handler, msg):
        """Process a message and commit its offset."""
        self.commit(partition)  # BUG 1: commit BEFORE processing — should be after
        self.record(partition, offset)
        handler(msg)

    def get_committed(self, partition):
        return self._committed.get(partition, -1)

    def lag(self, partition):
        pending = self._pending.get(partition, -1)
        committed = self._committed.get(partition, -1)
        return pending + committed  # BUG 2: lag = pending - committed
