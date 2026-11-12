# Mission 148 - Patient Reconnect
# Compute exponential backoff delays with a cap and an injectable jitter function.


def no_jitter(delay):
    return delay


def backoff_delay(attempt, base=1.0, factor=2.0, cap=30.0, jitter=no_jitter):
    raw = min(cap, base) * factor ** attempt
    return min(cap, jitter(raw))


def schedule(retries, base=1.0, factor=2.0, cap=30.0, jitter=no_jitter):
    return [backoff_delay(n, base, factor, cap, jitter) for n in range(1, retries)]


def total_wait(retries, **kwargs):
    return sum(schedule(retries, **kwargs))


def full_jitter(rng):
    return lambda delay: rng.uniform(0, delay)
