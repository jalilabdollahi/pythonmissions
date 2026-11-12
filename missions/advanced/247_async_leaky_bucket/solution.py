# Mission 247 - SMS Throttle (solution)
# Async leaky-bucket limiter with an injectable clock and sleep, plus per-tenant buckets.
import asyncio
import time


class LeakyBucket:
    """Holds up to `capacity` units; the level leaks away at `leak_rate` units per second."""

    def __init__(self, capacity, leak_rate, clock=time.monotonic, sleep=asyncio.sleep):
        if capacity <= 0 or leak_rate <= 0:
            raise ValueError("capacity and leak_rate must be positive")
        self.capacity = capacity
        self.leak_rate = leak_rate
        self._clock = clock
        self._sleep = sleep
        self.level = 0.0
        self._last = clock()
        self._lock = asyncio.Lock()
        self.total_wait = 0.0

    def _drain(self):
        now = self._clock()
        elapsed = now - self._last
        self.level = max(0.0, self.level - elapsed * self.leak_rate)
        self._last = now

    def _check_cost(self, cost):
        if cost <= 0 or cost > self.capacity:
            raise ValueError(f"cost must be in (0, {self.capacity}], got {cost}")

    def try_acquire(self, cost=1):
        self._check_cost(cost)
        self._drain()
        if self.level + cost > self.capacity:
            return False
        self.level += cost
        return True

    async def acquire(self, cost=1):
        self._check_cost(cost)
        async with self._lock:
            while True:
                self._drain()
                overflow = self.level + cost - self.capacity
                if overflow <= 0:
                    self.level += cost
                    return
                pause = overflow / self.leak_rate
                self.total_wait += pause
                await self._sleep(pause)

    def retry_after(self, cost=1):
        """Seconds until `cost` units would fit, without consuming anything."""
        self._check_cost(cost)
        self._drain()
        overflow = self.level + cost - self.capacity
        return max(0.0, overflow / self.leak_rate)


class TenantThrottle:
    def __init__(self, capacity, leak_rate, clock=time.monotonic, sleep=asyncio.sleep):
        self._args = (capacity, leak_rate, clock, sleep)
        self._buckets = {}

    def bucket(self, tenant):
        if tenant not in self._buckets:
            self._buckets[tenant] = LeakyBucket(*self._args)
        return self._buckets[tenant]

    async def send(self, tenant, deliver, message, cost=1):
        await self.bucket(tenant).acquire(cost)
        return await deliver(tenant, message)
