# Mission 062 - REST Client with Retry
# Fixed solution
import time

class RestClient:
    def __init__(self, session, max_retries=3, base_delay=0.0):
        self.session = session
        self.max_retries = max_retries
        self.base_delay = base_delay

    def get(self, url):
        last_error = None
        for attempt in range(self.max_retries):
            try:
                resp = self.session.get(url, timeout=10)
                if resp.status_code >= 500:
                    raise ValueError(f"HTTP {resp.status_code}")
                return resp
            except Exception as e:
                last_error = e
                delay = self.base_delay * (2 ** attempt)
                time.sleep(delay)
        raise last_error
