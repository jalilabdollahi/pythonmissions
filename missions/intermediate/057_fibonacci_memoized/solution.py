# Mission 057 - Memoized Fibonacci
# Fixed solution

_cache = {}

def fib(n):
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return 0
    if n == 1:
        return 1
    if n in _cache:
        return _cache[n]
    result = fib(n - 1) + fib(n - 2)
    _cache[n] = result
    return result
