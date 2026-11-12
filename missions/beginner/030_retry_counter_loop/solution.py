# Mission 030 - Endless Retry Spiral (solution)
# Retry a flaky call a bounded number of times with exponential backoff.


def call_with_retries(action, max_attempts=3, sleep=lambda seconds: None):
    attempts = 0
    last_error = None
    while attempts < max_attempts:
        try:
            return action()
        except ConnectionError as exc:
            last_error = exc
            attempts += 1
            sleep(2 ** (attempts - 1))
    raise RuntimeError(f"gave up after {attempts} attempts") from last_error


def export_invoices(fetch_page, pages, sleep=lambda seconds: None):
    return [call_with_retries(lambda p=p: fetch_page(p), sleep=sleep) for p in range(pages)]
