# Mission 186 - Bucket Of Tokens (solution)
# A token-bucket rate limiter driven by an injected clock.
class TokenBucket:
    def __init__(self, capacity, rate, clock):
        self.capacity = capacity
        self.rate = rate
        self.clock = clock
        self.tokens = float(capacity)
        self.last = clock()

    def _refill(self):
        now = self.clock()
        self.tokens = min(self.capacity, self.tokens + (now - self.last) * self.rate)
        self.last = now

    def allow(self, cost=1):
        self._refill()
        if self.tokens >= cost:
            self.tokens -= cost
            return True
        return False

    def retry_after(self, cost=1):
        self._refill()
        missing = cost - self.tokens
        if missing <= 0:
            return 0.0
        return missing / self.rate


def burst_size(bucket, limit=1000):
    count = 0
    while count < limit and bucket.allow():
        count += 1
    return count


def main():
    import time

    bucket = TokenBucket(capacity=5, rate=2.0, clock=time.monotonic)
    print("burst allowed:", burst_size(bucket))
    print("retry after: %.2fs" % bucket.retry_after())


if __name__ == "__main__":
    main()
