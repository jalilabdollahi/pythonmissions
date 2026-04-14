# Mission 102 - Solution
def retry_loop(max_retries, fn):
    attempt = 0
    while attempt < max_retries:
        result = fn(attempt)
        if result is not None:
            return result
        attempt += 1
    return None

if __name__ == "__main__":
    calls = []
    def fn(a):
        calls.append(a)
        return "ok" if len(calls) >= 3 else None
    print(retry_loop(5, fn))
