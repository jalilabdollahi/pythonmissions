# Mission 070 - Slots Class
# Fix the 2 bugs in this script.

class Metric:
    __slots__ = ["name", "value"]  # BUG 1: missing "timestamp" and "tags"

    def __init__(self, name, value, timestamp, tags=None):
        self.name = name
        self.value = value
        self.timestamp = timestamp
        self.tags = tags or {}

    def to_dict(self):
        return {
            "name": self.name,
            "value": self.value,
            "timestamp": self.timestamp,
            "tags": self.tags,
        }

    def __repr__(self):
        return f"Metric({self.name}={self.value} @ {self.timestamp})"
