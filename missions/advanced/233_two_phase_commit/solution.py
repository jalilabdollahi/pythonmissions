# Mission 233 - Cross-Region Booking Commit (solution)
# Two-phase commit coordinator across regional booking services.


class Participant:
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity
        self.reserved = {}
        self.committed = 0

    def available(self):
        return self.capacity - self.committed - sum(self.reserved.values())

    def prepare(self, txn_id, amount):
        if amount > self.available():
            return False
        self.reserved[txn_id] = amount
        return True

    def commit(self, txn_id):
        self.committed += self.reserved.pop(txn_id)

    def rollback(self, txn_id):
        self.reserved.pop(txn_id, None)


class Coordinator:
    def __init__(self, participants):
        self.participants = participants
        self.log = []

    def _abort(self, txn_id, prepared, reason):
        self.log.append((txn_id, "abort"))
        for name in reversed(prepared):
            self.participants[name].rollback(txn_id)
        return {"status": "aborted", "reason": reason, "commit_errors": []}

    def run(self, txn_id, plan):
        prepared = []
        for name, amount in plan.items():
            try:
                vote = self.participants[name].prepare(txn_id, amount)
            except Exception as exc:
                return self._abort(txn_id, prepared, f"{name} failed: {exc}")
            if not vote:
                return self._abort(txn_id, prepared, f"{name} voted no")
            prepared.append(name)
        self.log.append((txn_id, "commit"))
        errors = []
        for name in prepared:
            try:
                self.participants[name].commit(txn_id)
            except Exception as exc:
                errors.append((name, str(exc)))
        return {"status": "committed", "reason": None, "commit_errors": errors}

    def summary(self):
        return {
            name: {"free": p.available(), "committed": p.committed}
            for name, p in sorted(self.participants.items())
        }

    def decision(self, txn_id):
        for logged_id, outcome in reversed(self.log):
            if logged_id == txn_id:
                return outcome
        return None

    def in_doubt(self):
        return {
            name: sorted(p.reserved)
            for name, p in self.participants.items()
            if p.reserved
        }
