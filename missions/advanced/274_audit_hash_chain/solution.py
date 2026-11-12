# Mission 274 - Ledgerlight Tamper Seal (solution)
# Hash-chained audit log: each record commits to the previous one, so edits are detectable.
import hashlib
import json

GENESIS = "0" * 64


def record_hash(seq, ts, actor, action, prev_hash):
    """Hash an unambiguous encoding of every field of the record."""
    body = json.dumps([seq, ts, actor, action, prev_hash], separators=(",", ":"))
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


class AuditLog:
    def __init__(self):
        self.records = []

    @property
    def head(self):
        return self.records[-1]["hash"] if self.records else GENESIS

    def append(self, actor, action, ts):
        seq = len(self.records)
        prev = self.head
        self.records.append(
            {
                "seq": seq,
                "ts": ts,
                "actor": actor,
                "action": action,
                "prev": prev,
                "hash": record_hash(seq, ts, actor, action, prev),
            }
        )
        return self.records[-1]

    def export(self):
        return [dict(r) for r in self.records]


def verify_chain(records, anchor=None):
    """Return (ok, index_of_first_problem, reason).

    `anchor` is the head hash published somewhere the log writer cannot rewrite
    (a ticket, a notarization service). It detects truncation and full re-chaining.
    """
    prev = GENESIS
    for index, rec in enumerate(records):
        if rec["seq"] != index:
            return False, index, "sequence gap"
        if rec["prev"] != prev:
            return False, index, "broken link"
        expected = record_hash(rec["seq"], rec["ts"], rec["actor"], rec["action"], rec["prev"])
        if rec["hash"] != expected:
            return False, index, "record modified"
        prev = rec["hash"]
    if anchor is not None and prev != anchor:
        return False, len(records), "head does not match anchor"
    return True, None, "ok"


def rechain(records):
    """Recompute links and hashes in place, as an attacker with write access would."""
    prev = GENESIS
    for index, rec in enumerate(records):
        rec["seq"] = index
        rec["prev"] = prev
        rec["hash"] = record_hash(rec["seq"], rec["ts"], rec["actor"], rec["action"], prev)
        prev = rec["hash"]
    return records


def actors_between(records, start_ts, end_ts):
    """Distinct actors with activity in [start_ts, end_ts], after verifying the chain."""
    ok, index, reason = verify_chain(records)
    if not ok:
        raise ValueError(f"audit log corrupted at {index}: {reason}")
    return sorted({r["actor"] for r in records if start_ts <= r["ts"] <= end_ts})


if __name__ == "__main__":
    log = AuditLog()
    log.append("ana", "grant:admin", 1)
    log.append("bo", "delete:db", 2)
    print(verify_chain(log.export(), anchor=log.head))
