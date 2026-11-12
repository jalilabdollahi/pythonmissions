# Mission 253 - Build Farm Job Queue
# Priority queue whose waiting jobs gain urgency over time, so nothing starves.


class Job:
    def __init__(self, job_id, priority, enqueued_at, seq, not_before=0.0):
        self.id = job_id
        self.priority = priority  # lower number = more urgent
        self.enqueued_at = enqueued_at
        self.seq = seq
        self.not_before = not_before
        self.attempts = 0

    def __repr__(self):
        return f"Job({self.id!r}, p={self.priority})"


class AgingQueue:
    def __init__(self, clock, aging_rate=0.1, max_boost=5.0):
        self._clock = clock
        self.aging_rate = aging_rate
        self.max_boost = max_boost
        self._jobs = []
        self._seq = 0

    def push(self, job_id, priority, delay=0.0):
        now = self._clock()
        job = Job(job_id, priority, now, self._seq, not_before=now + delay)
        self._seq += 1
        self._jobs.append(job)
        return job

    def effective_priority(self, job, now=None):
        now = self._clock() if now is None else now
        waited = max(0.0, now - job.enqueued_at)
        boost = waited * self.aging_rate
        return job.priority - boost

    def _eligible(self, now):
        return list(self._jobs)

    def _best(self, now):
        candidates = self._eligible(now)
        if not candidates:
            return None
        return min(candidates, key=lambda j: (self.effective_priority(j, now), -j.seq))

    def peek(self):
        job = self._best(self._clock())
        return job.id if job else None

    def pop(self):
        job = self._best(self._clock())
        if job is None:
            return None
        self._jobs.remove(job)
        job.attempts += 1
        return job

    def requeue(self, job, delay=0.0):
        """Put a failed job back. It keeps the age and queue position it earned."""
        job.enqueued_at = self._clock()
        job.not_before = self._clock() + delay
        self._jobs.append(job)

    def cancel(self, job_id):
        before = len(self._jobs)
        self._jobs = [job for job in self._jobs if job.id != job_id]
        return len(self._jobs) != before

    def ranking(self):
        now = self._clock()
        rows = [(j.id, self.effective_priority(j, now)) for j in self._eligible(now)]
        return sorted(rows, key=lambda row: row[1])

    def __len__(self):
        return len(self._jobs)


def drain(queue):
    order = []
    while True:
        job = queue.pop()
        if job is None:
            return order
        order.append(job.id)
