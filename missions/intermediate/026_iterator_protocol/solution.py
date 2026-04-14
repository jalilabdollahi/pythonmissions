# Mission 026 - Log Iterator Protocol
# Fixed solution

class LogIterator:
    def __init__(self, logs):
        self.logs = logs
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.logs):
            raise StopIteration
        entry = self.logs[self.index]
        self.index += 1
        return entry
