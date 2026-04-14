# Mission 092 - Kafka Consumer Offset Tracker
# Fixed solution

class OffsetTracker:
    def __init__(self):
        self._committed = {}
        self._pending = {}

    def record(self, partition, offset):
        current = self._pending.get(partition, -1)
        if offset > current:
            self._pending[partition] = offset

    def commit(self, partition):
        if partition in self._pending:
            self._committed[partition] = self._pending[partition]
            del self._pending[partition]

    def process_message(self, partition, offset, handler, msg):
        self.record(partition, offset)
        handler(msg)
        self.commit(partition)

    def get_committed(self, partition):
        return self._committed.get(partition, -1)

    def lag(self, partition):
        pending = self._pending.get(partition, -1)
        committed = self._committed.get(partition, -1)
        return pending - committed
