# Mission 110 - Chaos Monkey Fault Injector
# Fixed solution
import random
import functools
import logging

logger = logging.getLogger(__name__)

def chaos(probability=0.1, exception=Exception, message="Chaos fault injected"):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if random.random() < probability:
                logger.warning(f"Chaos fault injected into {func.__name__}: {message}")
                raise exception(message)
            return func(*args, **kwargs)
        return wrapper
    return decorator
