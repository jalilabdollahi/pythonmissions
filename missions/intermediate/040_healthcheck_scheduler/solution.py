# Mission 040 - Healthcheck Scheduler
# Fixed solution
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
        for name, fn in self.services:
            self.results[name] = fn()

    def run_until(self, stop_after, clock=None):
        """Run checks until stop_after seconds have elapsed."""
        clock = clock or time.monotonic
        start = clock()
        next_run = start
        while clock() - start < stop_after:
            if clock() >= next_run:
                self.run_once()
                next_run = clock() + self.interval
            time.sleep(0.01)
