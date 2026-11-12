# Mission 231 - Zombie Writer Fence (solution)
# Lease lock service with fencing tokens and a store that rejects stale writers.


class StaleTokenError(Exception):
    pass


class LockService:
    def __init__(self, clock, lease_seconds=10.0):
        self.clock = clock
        self.lease_seconds = lease_seconds
        self.holder = None
        self.expires_at = 0.0
        self._counter = 0

    def _lease_live(self):
        return self.holder is not None and self.clock() < self.expires_at

    def acquire(self, client):
        now = self.clock()
        if self._lease_live():
            if self.holder != client:
                return None
            self.expires_at = now + self.lease_seconds
            return self._counter
        self._counter += 1
        self.holder = client
        self.expires_at = now + self.lease_seconds
        return self._counter

    def release(self, client, token):
        if self.holder == client and token == self._counter:
            self.holder = None
            return True
        return False

    def current_token(self):
        return self._counter if self._lease_live() else None


class FencedStore:
    def __init__(self):
        self.data = {}
        self.highest_token = 0
        self.log = []

    def write(self, key, value, token):
        if token < self.highest_token:
            raise StaleTokenError(
                f"token {token} is older than {self.highest_token}; writer lost its lease"
            )
        self.highest_token = max(self.highest_token, token)
        self.data[key] = value
        self.log.append((token, key))

    def read(self, key, default=None):
        return self.data.get(key, default)

    def writers_seen(self):
        return sorted({token for token, _ in self.log})


def run_job(service, store, client, key, value):
    token = service.acquire(client)
    if token is None:
        return "busy"
    try:
        store.write(key, value, token)
    except StaleTokenError:
        return "fenced"
    return "written"
