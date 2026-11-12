# Mission 232 - Scheduler Lease Heartbeat (solution)
# Leader lease with renewal, safety margin and a deterministic injected clock.


class LeaseStore:
    def __init__(self, clock, latency=0.0, sleep=None):
        self.clock = clock
        self.latency = latency
        self.sleep = sleep
        self.owner = None
        self.expires_at = 0.0

    def _delay(self):
        if self.sleep and self.latency:
            self.sleep(self.latency)

    def _free(self):
        return self.owner is None or self.clock() >= self.expires_at

    def acquire(self, node, duration):
        self._delay()
        if self._free() or self.owner == node:
            self.owner = node
            self.expires_at = self.clock() + duration
            return True
        return False

    def renew(self, node, duration):
        self._delay()
        if self.owner != node or self._free():
            return False
        self.expires_at = self.clock() + duration
        return True


class Elector:
    def __init__(self, node, store, clock, duration=15.0, margin=2.0, renew_every=5.0):
        self.node = node
        self.store = store
        self.clock = clock
        self.duration = duration
        self.margin = margin
        self.renew_every = renew_every
        self.deadline = None
        self.next_renew = None

    def is_leader(self):
        return self.deadline is not None and self.clock() < self.deadline

    def _granted(self, started):
        self.deadline = started + self.duration - self.margin
        self.next_renew = started + self.renew_every

    def _step_down(self):
        self.deadline = None
        self.next_renew = None

    def tick(self):
        now = self.clock()
        if not self.is_leader():
            started = now
            if self.store.acquire(self.node, self.duration):
                self._granted(started)
            else:
                self._step_down()
            return self.is_leader()
        if now >= self.next_renew:
            started = now
            if self.store.renew(self.node, self.duration):
                self._granted(started)
            else:
                self._step_down()
        return self.is_leader()


def dispatch(elector, jobs):
    if not elector.is_leader():
        return []
    return [f"{elector.node}:{job}" for job in jobs]
