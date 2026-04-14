# Mission 084 - Exponential Backoff
# Fixed solution
import random

def backoff_delay(attempt, base=0.1, cap=60.0, jitter=True):
    delay = base * (2 ** attempt)
    delay = min(delay, cap)
    if jitter:
        delay = delay + random.uniform(0, delay)
    return delay

def should_retry(attempt, max_attempts=5):
    return attempt < max_attempts
