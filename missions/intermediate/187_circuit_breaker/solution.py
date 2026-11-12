# Mission 187 - Trip The Breaker (solution)
# A circuit breaker with closed, open and half-open states and an injected clock.
class CircuitOpenError(Exception):
    pass


class CircuitBreaker:
    def __init__(self, failure_threshold, reset_timeout, clock):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.clock = clock
        self.state = "closed"
        self.failures = 0
        self.opened_at = None

    def _open(self):
        self.state = "open"
        self.opened_at = self.clock()
        self.failures = 0

    def call(self, fn):
        if self.state == "open":
            if self.clock() - self.opened_at >= self.reset_timeout:
                self.state = "half_open"
            else:
                raise CircuitOpenError("circuit is open")
        try:
            result = fn()
        except Exception:
            self.failures += 1
            if self.state == "half_open" or self.failures >= self.failure_threshold:
                self._open()
            raise
        self.failures = 0
        self.state = "closed"
        return result
