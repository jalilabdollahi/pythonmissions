# Mission 047 - Circuit Breaker
# Fix the 2 bugs in this script.
import time

class CircuitBreaker:
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.state = self.CLOSED
        self.failures = 0
        self.last_failure_time = None

    def call(self, fn, *args, **kwargs):
        if self.state == self.OPEN:
            if time.time() - self.last_failure_time > self.timeout:
                self.state = self.HALF_OPEN
            else:
                raise RuntimeError("Circuit is OPEN")
        try:
            result = fn(*args, **kwargs)
            if self.state == self.HALF_OPEN:
                self.failures += 1  # BUG 1: success in HALF_OPEN should reset/close
                self.state = self.CLOSED
            return result
        except Exception as e:
            self.failures += 1
            self.last_failure_time = time.time()
            if self.failures < self.failure_threshold:  # BUG 2: should be >=
                self.state = self.OPEN
            raise
