# Mission 249 - Tenant Quota Transfers (solution)
# Moves compute quota between tenants while many threads do it at once.
import threading
from contextlib import ExitStack


class InsufficientQuota(Exception):
    pass


class CapExceeded(Exception):
    pass


class Tenant:
    def __init__(self, tenant_id, quota, cap):
        self.id = tenant_id
        self.quota = quota
        self.cap = cap
        self.lock = threading.Lock()


class QuotaLedger:
    def __init__(self, tenants):
        self.tenants = {t.id: t for t in tenants}
        self.hook = None
        self.history = []
        self._history_lock = threading.Lock()

    def _signal(self, stage):
        if self.hook is not None:
            self.hook(stage)

    def transfer(self, src_id, dst_id, units):
        if units <= 0:
            raise ValueError("units must be positive")
        if src_id == dst_id:
            raise ValueError("cannot transfer quota to the same tenant")
        src = self.tenants[src_id]
        dst = self.tenants[dst_id]
        self._signal("validated")
        first, second = sorted((src, dst), key=lambda t: t.id)
        with first.lock:
            self._signal("first_locked")
            with second.lock:
                if src.quota < units:
                    raise InsufficientQuota(f"{src.id} has {src.quota}, needs {units}")
                if dst.quota + units > dst.cap:
                    raise CapExceeded(f"{dst.id} would exceed its cap of {dst.cap}")
                src.quota -= units
                dst.quota += units
        with self._history_lock:
            self.history.append((src_id, dst_id, units))

    def transfer_many(self, moves):
        """Apply moves in order; rejected ones are reported, not raised."""
        results = []
        for src_id, dst_id, units in moves:
            try:
                self.transfer(src_id, dst_id, units)
                results.append("ok")
            except (InsufficientQuota, CapExceeded) as exc:
                results.append(type(exc).__name__)
        return results

    def audit(self):
        """Consistent snapshot of every tenant's quota."""
        with ExitStack() as stack:
            for tenant in sorted(self.tenants.values(), key=lambda t: t.id):
                stack.enter_context(tenant.lock)
            return {t.id: t.quota for t in self.tenants.values()}

    def total(self):
        return sum(self.audit().values())

    def headroom(self, tenant_id):
        with self.tenants[tenant_id].lock:
            tenant = self.tenants[tenant_id]
            return tenant.cap - tenant.quota
