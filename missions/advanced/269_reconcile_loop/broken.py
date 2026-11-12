# Mission 269 - Pelican Reconciler
# A tiny controller: drive actual state to desired state, retrying transient failures with backoff.


class TransientError(Exception):
    """Worth retrying: timeouts, throttling, a dependency that is not ready yet."""


class PermanentError(Exception):
    """Retrying cannot help: invalid spec, forbidden, quota policy."""


class Controller:
    def __init__(self, backend, clock, base_delay=1.0, max_delay=30.0):
        self.backend = backend
        self.clock = clock
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.queue = {}  # key -> ready_at, at most one entry per key
        self.failures = {}  # key -> consecutive transient failures
        self.dead = {}  # key -> message of the permanent error

    def enqueue(self, key, delay=0.0):
        ready_at = self.clock() + delay
        if key in self.queue:
            self.queue[key] = min(self.queue[key], ready_at)
        else:
            self.queue[key] = ready_at

    def backoff(self, key):
        attempts = self.failures[key]
        return min(self.max_delay, self.base_delay * 2 ** attempts)

    def reconcile(self, key):
        desired = self.backend.desired[key]
        self.backend.apply(key, desired)
        return "applied"

    def run_once(self):
        """Process every key that is due now, in key order. Returns [(key, outcome)]."""
        now = self.clock()
        due = sorted(k for k, ready_at in self.queue.items() if ready_at <= now)
        results = []
        for key in due:
            del self.queue[key]
            try:
                outcome = self.reconcile(key)
            except TransientError:
                self.failures[key] = self.failures.get(key, 0) + 1
                self.enqueue(key, self.backoff(key))
                outcome = "requeued"
            except PermanentError as exc:
                self.failures.pop(key, None)
                self.dead[key] = str(exc)
                self.enqueue(key, self.max_delay)
                outcome = "failed"
            else:
                pass
            results.append((key, outcome))
        return results


class FakeBackend:
    """In-memory cloud. `script[key]` is a list of exceptions to raise on successive applies."""

    def __init__(self, desired, actual=None, script=None):
        self.desired = dict(desired)
        self.actual = dict(actual or {})
        self.script = {k: list(v) for k, v in (script or {}).items()}
        self.apply_calls = []

    def read(self, key):
        return self.actual.get(key)

    def apply(self, key, spec):
        self.apply_calls.append(key)
        pending = self.script.get(key)
        if pending:
            raise pending.pop(0)
        self.actual[key] = spec


if __name__ == "__main__":
    now = [0.0]
    backend = FakeBackend({"web": {"replicas": 3}})
    ctl = Controller(backend, lambda: now[0])
    ctl.enqueue("web")
    print(ctl.run_once())
