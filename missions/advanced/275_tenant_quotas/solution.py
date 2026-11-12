# Mission 275 - Quotas Without Crosstalk (solution)
# Per-tenant resource quotas for a shared build platform. One tenant must never affect another.

DEFAULT_LIMITS = {"cpu": 16, "memory_gb": 64, "disks": 10}


class QuotaExceeded(Exception):
    def __init__(self, tenant, resource, wanted, available):
        super().__init__(f"{tenant}: {resource} needs {wanted}, only {available} left")
        self.resource = resource


class Tenant:
    def __init__(self, name, limits=None, history=None):
        self.name = name
        self.history = [] if history is None else history
        self.limits = dict(DEFAULT_LIMITS)
        self.limits.update(limits or {})
        self.used = {resource: 0 for resource in self.limits}

    def available(self, resource):
        return self.limits[resource] - self.used[resource]

    def reserve(self, request):
        """Reserve every resource in `request` or none of them."""
        for resource, amount in request.items():
            if amount < 0:
                raise ValueError("cannot reserve a negative amount")
            if resource not in self.limits:
                raise KeyError(f"unknown resource {resource}")
        for resource, amount in request.items():
            if amount > self.available(resource):
                raise QuotaExceeded(self.name, resource, amount, self.available(resource))
        for resource, amount in request.items():
            self.used[resource] += amount
        self.history.append(("reserve", dict(request)))

    def release(self, request):
        for resource, amount in request.items():
            self.used[resource] = max(0, self.used[resource] - amount)
        self.history.append(("release", dict(request)))

    def utilization(self):
        return {r: round(self.used[r] / self.limits[r], 3) for r in sorted(self.limits) if self.limits[r]}


class QuotaManager:
    def __init__(self):
        self.tenants = {}

    def register(self, name, limits=None):
        if name in self.tenants:
            raise ValueError(f"tenant {name} already registered")
        self.tenants[name] = Tenant(name, limits)
        return self.tenants[name]

    def reserve(self, name, request):
        self.tenants[name].reserve(request)

    def release(self, name, request):
        self.tenants[name].release(request)

    def noisy_tenants(self, threshold=0.8):
        return sorted(
            name
            for name, tenant in self.tenants.items()
            if any(u >= threshold for u in tenant.utilization().values())
        )


if __name__ == "__main__":
    mgr = QuotaManager()
    mgr.register("ci-team", {"cpu": 4})
    mgr.reserve("ci-team", {"cpu": 3})
    print(mgr.noisy_tenants())
