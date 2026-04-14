# Mission 084 - Exponential Backoff
# Fix the 2 bugs in this script.
import random

def backoff_delay(attempt, base=0.1, cap=60.0, jitter=True):
    """Calculate delay for given attempt number (0-indexed)."""
    delay = base * attempt  # BUG 1: should be base * (2 ** attempt)
    delay = min(delay, cap)
    if jitter:
        delay = delay  # BUG 2: should add jitter: delay + random.uniform(0, delay)
    return delay

def should_retry(attempt, max_attempts=5):
    return attempt < max_attempts
