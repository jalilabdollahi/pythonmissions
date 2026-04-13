# Mission 11 - Retry Logic Decorator
# Fix the 2 bugs in this script.

import functools
import time


def retry(max_attempts=3, delay=1.0):
    def decorator(func):
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    print(f"Attempt {attempt}/{max_attempts} failed: {e}")
                    time.sleep(delay)
            raise last_error
        return wrapper
    return decorator


@retry(max_attempts=3, delay=0.01)
def fetch_config(service_name):
    """Fetch configuration for a service from the config server."""
    raise ConnectionError(f"Config server unreachable for {service_name}")


@retry(max_attempts=2, delay=0.01)
def get_secret(key):
    """Retrieve a secret from the vault."""
    return f"secret-value-for-{key}"


if __name__ == "__main__":
    try:
        fetch_config("api-gateway")
    except ConnectionError as e:
        print(f"All retries exhausted: {e}")

    value = get_secret("DB_PASSWORD")
    print(f"Secret: {value}")
