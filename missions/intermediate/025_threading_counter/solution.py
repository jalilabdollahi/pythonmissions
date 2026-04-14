# Mission 025 - Thread-Safe Counter
# Fixed solution
import threading

class Counter:
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:
            self.value += 1

    def decrement(self):
        with self.lock:
            self.value -= 1

    def reset(self):
        with self.lock:
            self.value = 0

    def get(self):
        with self.lock:
            return self.value
