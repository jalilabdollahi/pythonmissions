# Mission 149 - Retry Wrapper
# A decorator that retries transient failures with a pause between attempts.
import time


def retry(attempts, retry_on=(ConnectionError,), delay=0.5, sleep=time.sleep):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(1, attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == attempts:
                        return None
                    sleep(delay)

        return wrapper

    return decorator


@retry(attempts=3, retry_on=(ConnectionError, TimeoutError), delay=1)
def fetch_invoice_batch(client, batch_id):
    """Download one batch of invoices."""
    return client(batch_id)
