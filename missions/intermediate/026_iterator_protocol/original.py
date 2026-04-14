# Mission 026 - Log Iterator Protocol
# Fix the 2 bugs in this script.

class LogIterator:
    def __init__(self, logs):
        self.logs = logs
        self.index = 0

    def __iter__(self):
        return LogIterator(self.logs)  # BUG 1: should return self

    def __next__(self):
        if self.index >= len(self.logs):
            return None  # BUG 2: should raise StopIteration
        entry = self.logs[self.index]
        self.index += 1
        return entry
