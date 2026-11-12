# Mission 284 - Poison Pill Parking
# Message broker that retries failed deliveries and parks poison messages in a dead-letter queue.
from collections import deque


class PermanentError(Exception):
    """Raised by a handler when retrying can never help (bad schema, unknown tenant)."""


class Message:
    def __init__(self, msg_id, body):
        self.id = msg_id
        self.body = body
        self.attempts = 0
        self.errors = []


class Broker:
    def __init__(self, max_attempts=3):
        self.max_attempts = max_attempts
        self.queue = deque()
        self.dead = []
        self.processed = []

    def publish(self, msg_id, body):
        self.queue.append(Message(msg_id, body))

    def run(self, handler, max_deliveries=1000):
        """Deliver until the queue is empty. Returns the number of deliveries made."""
        deliveries = 0
        while self.queue and deliveries < max_deliveries:
            msg = self.queue.popleft()
            deliveries += 1
            msg.attempts += 1
            try:
                handler(msg.body)
            except Exception as exc:
                msg.errors.append(str(exc))
                if type(exc) is PermanentError:
                    self._park(msg, "permanent")
                elif msg.attempts > self.max_attempts:
                    self._park(msg, "retries_exhausted")
                else:
                    self.queue.appendleft(msg)
            else:
                self.processed.append(msg.id)
        return deliveries

    def _park(self, msg, reason):
        self.dead.append({
            "id": msg.id,
            "body": msg.body,
            "reason": reason,
            "attempts": msg.attempts,
            "last_error": msg.errors[0],
        })

    def redrive(self, reason=None):
        """Move parked messages back to the queue with a fresh attempt budget."""
        keep, moved = [], 0
        for entry in self.dead:
            if reason is None or entry["reason"] == reason:
                self.queue.append(Message(entry["id"], entry["body"]))
                moved += 1
            else:
                keep.append(entry)
        self.dead = keep
        return moved

    def summary(self):
        return {
            "processed": len(self.processed),
            "dead": len(self.dead),
            "queued": len(self.queue),
        }
