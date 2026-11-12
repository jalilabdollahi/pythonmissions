# Mission 296 - Drain And Exit (solution)
# Graceful shutdown: stop accepting work, drain the queue until a deadline, then exit.
from collections import deque


class Server:
    def __init__(self, clock, grace=30):
        self.clock = clock
        self.grace = grace
        self.queue = deque()
        self.accepting = True
        self.deadline = None
        self.force = False
        self.done = []
        self.failed = []
        self.abandoned = []
        self.rejected = []

    def submit(self, job_id, fn):
        """Queue a job. Returns False when the server is shutting down."""
        if not self.accepting:
            self.rejected.append(job_id)
            return False
        self.queue.append((job_id, fn))
        return True

    def handle_signal(self, signum=15):
        """SIGTERM handler body. The first signal starts a drain, a second forces exit."""
        if self.deadline is not None:
            self.force = True
            return "force"
        self.accepting = False
        self.deadline = self.clock() + self.grace
        return "draining"

    def drain(self):
        """Run queued jobs until the queue is empty, the deadline passes or a second signal
        arrives. Returns the process exit code: 0 for a clean drain, 1 otherwise."""
        if self.deadline is None:
            self.handle_signal()
        while self.queue:
            if self.force or self.clock() >= self.deadline:
                self.abandoned.extend(job_id for job_id, _ in self.queue)
                self.queue.clear()
                break
            job_id, fn = self.queue.popleft()
            try:
                fn()
                self.done.append(job_id)
            except Exception:
                self.failed.append(job_id)
        return 0 if not (self.abandoned or self.failed) else 1

    def report(self):
        return {
            "done": list(self.done),
            "failed": list(self.failed),
            "abandoned": list(self.abandoned),
            "rejected": list(self.rejected),
        }


if __name__ == "__main__":
    import signal
    import time

    server = Server(time.monotonic)
    signal.signal(signal.SIGTERM, lambda signum, frame: server.handle_signal(signum))
    server.submit("demo", lambda: print("working"))
    raise SystemExit(server.drain())
