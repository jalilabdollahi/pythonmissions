# Mission 150 - Stopwatch Decorator (solution)
# Record how long each call of a pipeline stage takes without changing its result.
import functools
import time


def timed(sink, clock=None):
    clock = clock or time.perf_counter

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = clock()
            result = func(*args, **kwargs)
            sink.append((func.__name__, clock() - start))
            return result

        return wrapper

    return decorator


def slowest(sink):
    if not sink:
        return None
    return max(sink, key=lambda item: item[1])[0]


def total_by_stage(sink):
    totals = {}
    for name, seconds in sink:
        totals[name] = totals.get(name, 0) + seconds
    return totals
