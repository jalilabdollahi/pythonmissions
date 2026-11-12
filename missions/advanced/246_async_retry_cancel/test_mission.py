import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from broken import RetryExhausted, RetryPolicy, call_with_retry, charge_card, retrying, total_backoff


class Clock:
    def __init__(self):
        self.now = 0.0
        self.sleeps = []

    def __call__(self):
        return self.now

    async def sleep(self, seconds):
        self.sleeps.append(seconds)
        self.now += seconds


class Gateway:
    def __init__(self, failures, error=ConnectionError):
        self.failures = failures
        self.error = error
        self.calls = 0

    async def charge(self, amount):
        self.calls += 1
        if self.calls <= self.failures:
            raise self.error("gateway unavailable")
        return {"amount": amount, "attempt": self.calls}


def drive(coro, timeout=2):
    return asyncio.run(asyncio.wait_for(coro, timeout))


def test_succeeds_after_transient_failures_with_exponential_backoff():
    clock = Clock()
    gateway = Gateway(failures=3)
    policy = RetryPolicy(attempts=5, base_delay=0.5, factor=2.0, max_delay=8.0)
    receipt = drive(charge_card(gateway, 40, policy, clock.sleep, clock))
    assert receipt == {"amount": 40, "attempt": 4}
    assert clock.sleeps == [0.5, 1.0, 2.0], "delays start at base_delay and double"


def test_delay_is_capped_at_max_delay():
    policy = RetryPolicy(base_delay=1.0, factor=3.0, max_delay=5.0)
    assert [policy.delay_after(n) for n in (1, 2, 3, 4)] == [1.0, 3.0, 5.0, 5.0]


def test_no_sleep_after_the_final_failed_attempt():
    clock = Clock()
    gateway = Gateway(failures=99)
    with pytest.raises(RetryExhausted) as info:
        drive(charge_card(gateway, 1, RetryPolicy(attempts=3, base_delay=1.0), clock.sleep, clock))
    assert info.value.attempts == 3 and gateway.calls == 3
    assert clock.sleeps == [1.0, 2.0], "waiting after the last attempt only delays the error"
    assert isinstance(info.value.last_error, ConnectionError)


def test_non_retryable_errors_propagate_immediately():
    clock = Clock()
    gateway = Gateway(failures=99, error=ValueError)
    with pytest.raises(ValueError):
        drive(charge_card(gateway, 1, RetryPolicy(attempts=5), clock.sleep, clock))
    assert gateway.calls == 1 and clock.sleeps == []


def test_time_budget_stops_retrying_before_a_sleep_that_would_exceed_it():
    clock = Clock()
    gateway = Gateway(failures=99)
    policy = RetryPolicy(attempts=10, base_delay=1.0, factor=2.0, max_delay=100, budget=5.0)
    with pytest.raises(RetryExhausted) as info:
        drive(charge_card(gateway, 1, policy, clock.sleep, clock))
    assert clock.sleeps == [1.0, 2.0], "sleeping 4s at t=3 would end at t=7, past the 5s budget"
    assert clock.now <= 5.0
    assert info.value.attempts == 3


def test_cancellation_is_never_swallowed_or_retried():
    async def scenario():
        clock = Clock()
        started = asyncio.Event()
        release = asyncio.Event()
        calls = 0

        async def hang():
            nonlocal calls
            calls += 1
            started.set()
            await release.wait()

        task = asyncio.ensure_future(call_with_retry(hang, RetryPolicy(attempts=5), clock.sleep, clock))
        try:
            await started.wait()
            task.cancel()
            done, _ = await asyncio.wait({task}, timeout=1)
            assert done, "a cancelled retry loop must stop instead of calling the function again"
            assert task.cancelled()
            assert calls == 1
        finally:
            release.set()  # lets a misbehaving implementation finish so the test run can exit

    drive(scenario())


def test_decorator_passes_arguments_and_retries():
    clock = Clock()
    seen = []

    @retrying(RetryPolicy(attempts=3, base_delay=0.1), clock.sleep, clock)
    async def fetch(path, *, region):
        seen.append((path, region))
        if len(seen) < 2:
            raise TimeoutError("slow")
        return path.upper()

    assert drive(fetch("/ledger", region="eu")) == "/LEDGER"
    assert seen == [("/ledger", "eu")] * 2


def test_on_retry_hook_sees_each_wait_and_total_backoff_matches():
    clock = Clock()
    events = []
    gateway = Gateway(failures=2)
    policy = RetryPolicy(attempts=4, base_delay=1.0)
    drive(call_with_retry(lambda: gateway.charge(5), policy, clock.sleep, clock,
                          on_retry=lambda n, d, e: events.append((n, d, type(e).__name__))))
    assert events == [(1, 1.0, "ConnectionError"), (2, 2.0, "ConnectionError")]
    assert total_backoff(policy) == 1.0 + 2.0 + 4.0
