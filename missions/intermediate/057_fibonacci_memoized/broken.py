# Mission 057 - Memoized Fibonacci
# Fix the 2 bugs in this script.

_cache = {}

def fib(n):
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return 1  # BUG 1: fib(0) should be 0
    if n == 1:
        return 1
    if n in _cache:
        return _cache[n]
    result = fib(n - 1) + fib(n - 2)
    _cache[n] = result
    return _cache[n + 1]  # BUG 2: should return result (or _cache[n])
