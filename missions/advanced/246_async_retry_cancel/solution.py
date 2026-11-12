# Mission 246 - Payment Gateway Retry (solution)
# Async retry helper with exponential backoff, a time budget and clean cancellation.
import asyncio
import functools
import time


class RetryExhausted(Exception):
    def __init__(self, attempts, last_error):
        super().__init__(f"gave up after {attempts} attempts: {last_error!r}")
        self.attempts = attempts
        self.last_error = last_error


class RetryPolicy:
    def __init__(self, attempts=4, base_delay=0.5, factor=2.0, max_delay=8.0,
                 retry_on=(ConnectionError, TimeoutError), budget=None):
        if attempts < 1:
            raise ValueError("attempts must be at least 1")
        self.attempts = attempts
        self.base_delay = base_delay
        self.factor = factor
        self.max_delay = max_delay
        self.retry_on = retry_on
        self.budget = budget

    def __repr__(self):
        return (f"RetryPolicy(attempts={self.attempts}, base_delay={self.base_delay}, "
                f"factor={self.factor}, max_delay={self.max_delay}, budget={self.budget})")

    def delay_after(self, attempt):
        """Seconds to wait after the given failed attempt (1-based)."""
        return min(self.max_delay, self.base_delay * self.factor ** (attempt - 1))


async def call_with_retry(fn, policy, sleep=asyncio.sleep, clock=time.monotonic, on_retry=None):
    started = clock()
    last_error = None
    attempt = 0
    while attempt < policy.attempts:
        attempt += 1
        try:
            return await fn()
        except policy.retry_on as exc:
            last_error = exc
        if attempt == policy.attempts:
            break
        delay = policy.delay_after(attempt)
        if policy.budget is not None and clock() - started + delay > policy.budget:
            break
        if on_retry is not None:
            on_retry(attempt, delay, last_error)
        await sleep(delay)
    raise RetryExhausted(attempt, last_error) from last_error


def total_backoff(policy):
    """Worst-case time spent sleeping if every attempt fails."""
    return sum(policy.delay_after(n) for n in range(1, policy.attempts))


def retrying(policy, sleep=asyncio.sleep, clock=time.monotonic):
    def decorate(fn):
        @functools.wraps(fn)
        async def wrapper(*args, **kwargs):
            return await call_with_retry(lambda: fn(*args, **kwargs), policy, sleep, clock)

        return wrapper

    return decorate


async def charge_card(gateway, amount, policy, sleep=asyncio.sleep, clock=time.monotonic):
    """Charge through a flaky gateway; returns the receipt or raises RetryExhausted."""
    return await call_with_retry(lambda: gateway.charge(amount), policy, sleep, clock)
