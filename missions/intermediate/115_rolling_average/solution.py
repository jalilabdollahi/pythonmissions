# Mission 115 - Rolling Average
# Fixed solution
from collections import deque

class RollingAverage:
    def __init__(self, window=10):
        self.window = window
        self._values = deque(maxlen=window)

    def add(self, value):
        self._values.append(value)

    def average(self):
        if not self._values:
            return 0.0
        return sum(self._values) / len(self._values)

    def count(self):
        return len(self._values)
