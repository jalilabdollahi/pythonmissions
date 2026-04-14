# Mission 110 - Chaos Monkey Fault Injector
# Fix the 2 bugs in this script.
import random
import functools
import logging

logger = logging.getLogger(__name__)

def chaos(probability=0.1, exception=Exception, message="Chaos fault injected"):
    """Decorator that randomly raises exceptions."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if random.random() > probability:  # BUG 1: should be < probability
                raise exception(message)
            return func(*args, **kwargs)  # BUG 2: should log before raising
        return wrapper
    return decorator
