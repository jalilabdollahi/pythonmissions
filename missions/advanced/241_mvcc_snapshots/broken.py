# Mission 241 - Ledger Snapshot Reads
# Tiny multi-version row store with snapshot-isolated transactions.


class WriteConflict(Exception):
    pass


class Version:
    def __init__(self, value, creator):
        self.value = value
        self.creator = creator
        self.deleter = None


class Txn:
    def __init__(self, txid, snapshot):
        self.id = txid
        self.snapshot = snapshot
        self.status = "active"


class MVCCStore:
    def __init__(self):
        self.clock = 0
        self.next_txid = 1
        self.commit_ts = {}
        self.rows = {}
        self.active = {}

    def begin(self):
        txn = Txn(self.next_txid, self.clock)
        self.next_txid += 1
        self.active[txn.id] = txn
        return txn

    def _committed_by(self, txid, snapshot):
        ts = self.commit_ts.get(txid)
        return ts is not None and ts < snapshot

    def _visible(self, version, txn):
        mine = version.creator == txn.id
        if not (mine or self._committed_by(version.creator, txn.snapshot)):
            return False
        if version.deleter is None:
            return True
        deleted = self._committed_by(version.deleter, txn.snapshot)
        return not deleted

    def get(self, txn, key):
        for version in reversed(self.rows.get(key, [])):
            if self._visible(version, txn):
                return version.value
        return None

    def _head(self, key):
        for version in reversed(self.rows.get(key, [])):
            if version.creator in self.commit_ts or version.creator in self.active:
                return version
        return None

    def _check_conflict(self, txn, head):
        if head.creator != txn.id and not self._committed_by(head.creator, txn.snapshot):
            raise WriteConflict("row was created by a transaction outside our snapshot")
        deleter = head.deleter
        if deleter is None or deleter == txn.id:
            return
        if self.commit_ts.get(deleter, 0) > txn.snapshot:
            raise WriteConflict("row is being changed by another transaction")

    def put(self, txn, key, value):
        head = self._head(key)
        if head is not None:
            self._check_conflict(txn, head)
            if head.deleter is None:
                head.deleter = txn.id
        self.rows.setdefault(key, []).append(Version(value, txn.id))

    def delete(self, txn, key):
        head = self._head(key)
        if head is None:
            return False
        self._check_conflict(txn, head)
        if head.deleter is not None:
            return False
        head.deleter = txn.id
        return True

    def commit(self, txn):
        self.clock += 1
        self.commit_ts[txn.id] = self.clock
        txn.status = "committed"
        del self.active[txn.id]

    def abort(self, txn):
        txn.status = "aborted"
        del self.active[txn.id]
        for versions in self.rows.values():
            for version in versions:
                if version.deleter == txn.id:
                    version.deleter = None

    def vacuum(self):
        horizon = max((t.snapshot for t in self.active.values()), default=self.clock)
        removed = 0
        for key, versions in list(self.rows.items()):
            keep = []
            for version in versions:
                dead = version.creator not in self.commit_ts and version.creator not in self.active
                gone = version.deleter in self.commit_ts and self.commit_ts[version.deleter] <= horizon
                if dead or gone:
                    removed += 1
                else:
                    keep.append(version)
            self.rows[key] = keep
        return removed
