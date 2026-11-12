# Mission 236 - Payout Retry Guard
# Idempotency-key store for a payout API: replay, conflict detection, TTL expiry.
import hashlib
import json


class KeyConflict(Exception):
    pass


def fingerprint(payload):
    canonical = json.dumps(payload, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


class IdempotencyStore:
    def __init__(self, clock, ttl=86400.0):
        self.clock = clock
        self.ttl = ttl
        self.records = {}

    def _purge_expired(self):
        now = self.clock()
        for slot in [s for s, r in self.records.items() if now - r["created"] >= self.ttl]:
            del self.records[slot]

    def execute(self, tenant, key, payload, handler):
        self._purge_expired()
        slot = key
        digest = fingerprint(payload)
        record = self.records.get(slot)
        if record is not None:
            if record["state"] == "in_progress":
                raise KeyConflict(f"key {key!r} is still being processed")
            return record["response"], True
        self.records[slot] = {
            "fingerprint": digest,
            "state": "in_progress",
            "response": None,
            "created": self.clock(),
        }
        try:
            response = handler(payload)
        except Exception:
            raise
        self.records[slot].update(state="done", response=response)
        return response, False

    def status(self, tenant, key):
        self._purge_expired()
        record = self.records.get((tenant, key))
        return None if record is None else record["state"]

    def forget_tenant(self, tenant):
        doomed = [slot for slot in self.records if slot[0] == tenant]
        for slot in doomed:
            del self.records[slot]
        return len(doomed)

    def size(self):
        self._purge_expired()
        return len(self.records)


class PayoutService:
    def __init__(self, store):
        self.store = store
        self.ledger = []

    def _pay(self, payload):
        receipt = {"receipt": f"rcpt-{len(self.ledger) + 1}", "amount": payload["amount"]}
        self.ledger.append((payload["account"], payload["amount"]))
        return receipt

    def create_payout(self, tenant, key, payload):
        return self.store.execute(tenant, key, payload, self._pay)
