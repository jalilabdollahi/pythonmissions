# Mission 062 - REST Client with Retry
# Fix the 2 bugs in this script.
import time

class RestClient:
    def __init__(self, session, max_retries=3, base_delay=0.1):
        self.session = session
        self.max_retries = max_retries
        self.base_delay = base_delay

    def get(self, url):
        last_error = None
        for attempt in range(self.max_retries):
            try:
                resp = self.session.get(url, timeout=10)
                if resp.status_code >= 400:  # BUG 1: should only retry 5xx, not 4xx
                    raise ValueError(f"HTTP {resp.status_code}")
                return resp
            except Exception as e:
                last_error = e
                delay = self.base_delay * attempt  # BUG 2: should be 2**attempt for exponential
                time.sleep(delay)
        raise last_error
