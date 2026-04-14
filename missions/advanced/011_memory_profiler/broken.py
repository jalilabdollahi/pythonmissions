# Mission 011 (Advanced) - Memory Profiler
# Fix the 2 bugs in this script.
import tracemalloc
import functools

def profile_memory(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        result = func(*args, **kwargs)
        current, peak = tracemalloc.get_traced_memory()
        baseline = current  # BUG 1: baseline should be measured BEFORE calling func
        tracemalloc.stop()
        peak_kb = peak * 1024  # BUG 2: should be peak / 1024 to convert bytes to KB
        wrapper.last_peak_kb = peak_kb
        return result
    wrapper.last_peak_kb = 0
    return wrapper

@profile_memory
def allocate_list(n):
    return [i * i for i in range(n)]
