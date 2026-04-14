# Mission 011 (Advanced) - Memory Profiler
# Fixed solution
import tracemalloc
import functools

def profile_memory(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        baseline, _ = tracemalloc.get_traced_memory()
        result = func(*args, **kwargs)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        peak_kb = (peak - baseline) / 1024
        wrapper.last_peak_kb = peak_kb
        return result
    wrapper.last_peak_kb = 0
    return wrapper

@profile_memory
def allocate_list(n):
    return [i * i for i in range(n)]
