# Mission 039 - Circular Log Buffer
# Fixed solution

class CircularBuffer:
    def __init__(self, capacity):
        self.capacity = capacity
        self.buffer = [None] * capacity
        self.write_idx = 0
        self.size = 0

    def write(self, item):
        self.buffer[self.write_idx] = item
        self.write_idx = (self.write_idx + 1) % self.capacity
        if self.size < self.capacity:
            self.size += 1

    def read_all(self):
        if self.size < self.capacity:
            return self.buffer[:self.size]
        start = self.write_idx
        return self.buffer[start:] + self.buffer[:start]

    def is_full(self):
        return self.size >= self.capacity
