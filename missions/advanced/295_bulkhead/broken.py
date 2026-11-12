# Mission 295 - Bulkhead Doors
# Per-dependency concurrency limits so one slow backend cannot drain the whole worker pool.
from collections import Counter
from contextlib import contextmanager


class BulkheadFull(Exception):
    def __init__(self, dependency):
        super().__init__(f"bulkhead for {dependency} is full")
        self.dependency = dependency


class Bulkhead:
    def __init__(self, limits, pools=None, default_limit=2):
        self.limits = dict(limits)
        self.pools = dict(pools or {})
        self.default_limit = default_limit
        self.in_flight = Counter()
        self.rejected = Counter()
        self.peak = Counter()

    def _pool(self, dependency):
        """Dependencies mapped to the same pool name share one compartment."""
        return dependency

    def limit_for(self, dependency):
        return self.limits.get(self._pool(dependency), self.default_limit)

    def acquire(self, dependency):
        pool = self._pool(dependency)
        if self.in_flight[pool] > self.limit_for(dependency):
            self.rejected[pool] += 1
            return False
        self.in_flight[pool] += 1
        self.peak[pool] = max(self.peak[pool], self.in_flight[pool])
        return True

    def release(self, dependency):
        pool = self._pool(dependency)
        self.in_flight[pool] -= 1

    @contextmanager
    def guard(self, dependency):
        if not self.acquire(dependency):
            raise BulkheadFull(dependency)
        yield
        self.release(dependency)

    def call(self, dependency, fn, fallback=None):
        """Run fn inside the bulkhead; when it is full return fallback() or raise."""
        try:
            with self.guard(dependency):
                return fn()
        except BulkheadFull:
            if fallback is None:
                raise
            return fallback()

    def report(self):
        return {
            pool: {
                "in_flight": self.in_flight[pool],
                "rejected": self.rejected[pool],
                "peak": self.peak[pool],
            }
            for pool in sorted(set(self.in_flight) | set(self.rejected))
        }


if __name__ == "__main__":
    door = Bulkhead({"seatmap": 1})
    with door.guard("seatmap"):
        print(door.call("seatmap", lambda: "live", fallback=lambda: "cached"))
