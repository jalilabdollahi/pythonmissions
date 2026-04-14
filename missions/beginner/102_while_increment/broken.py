# Mission 102 - Retry with Backoff Counter
def retry_loop(max_retries, fn):
    """Call fn up to max_retries times. Return result or None."""
    attempt = 0
    while attempt < max_retries:
        result = fn(attempt)
        if result is not None:
            return result
    return None

if __name__ == "__main__":
    calls = []
    def fn(a):
        calls.append(a)
        return "ok" if len(calls) >= 3 else None
    print(retry_loop(5, fn))
