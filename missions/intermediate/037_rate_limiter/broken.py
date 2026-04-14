# Mission 037 - Token Bucket Rate Limiter
# Fix the 2 bugs in this script.
import time

class TokenBucket:
    def __init__(self, max_tokens, refill_rate):
        self.max_tokens = max_tokens
        self.tokens = max_tokens
        self.refill_rate = refill_rate  # tokens per second
        self.last_refill = time.monotonic()

    def _refill(self):
        now = time.monotonic()
        elapsed = now - self.last_refill
        new_tokens = elapsed * self.refill_rate
        self.tokens += new_tokens  # BUG 1: no cap at max_tokens
        self.last_refill = now

    def consume(self, tokens=1):
        self._refill()
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False  # BUG 2: missing — if not enough tokens, return False (this is actually correct already — bug is above)

    def available(self):
        self._refill()
        return int(self.tokens)
