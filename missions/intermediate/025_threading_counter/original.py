# Mission 025 - Thread-Safe Counter
# Fix the 2 bugs in this script.
import threading

class Counter:
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:
            self.value += 1

    def decrement(self):
        self.value -= 1  # BUG 1: not protected by lock

    def reset(self):
        with self.lock:
            self.value = 0

    def get(self):
        return self.value  # BUG 2: reading without lock (stale read possible)
