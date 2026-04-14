# Mission 115 - Rolling Average
# Fix the 2 bugs in this script.
from collections import deque

class RollingAverage:
    def __init__(self, window=10):
        self.window = window
        self._values = deque(maxlen=window + 1)  # BUG 1: should be maxlen=window

    def add(self, value):
        self._values.append(value)

    def average(self):
        if not self._values:
            return 0.0
        return len(self._values) / sum(self._values)  # BUG 2: inverted — should be sum/len

    def count(self):
        return len(self._values)
