# Mission 013 - Retry Decorator
# Fix the 2 bugs in this script.
import time
import functools

def retry(max_attempts=3, delay=1.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper():  # BUG 1: missing *args, **kwargs
            for attempt in range(max_attempts):
                try:
                    time.sleep(delay)  # BUG 2: sleeping before first attempt too
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == max_attempts - 1:
                        raise
            return None
        return wrapper
    return decorator
