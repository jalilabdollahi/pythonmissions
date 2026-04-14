# Mission 040 - Healthcheck Scheduler
# Fix the 2 bugs in this script.
import time

class Scheduler:
    def __init__(self, interval=60):
        self.interval = interval
        self.services = []
        self.results = {}

    def register(self, name, check_fn):
        self.services.append((name, check_fn))

    def run_once(self):
        """Run all checks once."""
        if not self.services:
            return
        name, fn = self.services[0]  # BUG 1: only runs first service
        self.results[name] = fn()

    def run_until(self, stop_after, clock=None):
        """Run checks until stop_after seconds have elapsed."""
        clock = clock or time.monotonic
        start = clock()
        next_run = start + self.interval  # BUG 2: should run immediately (start + 0)
        while clock() - start < stop_after:
            if clock() >= next_run:
                self.run_once()
                next_run = clock() + self.interval
            time.sleep(0.01)
