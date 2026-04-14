# Mission 029 (Advanced) - Multi-Tenant Isolation
# Fix the 2 bugs in this script.

class TenantManager:
    def __init__(self):
        self._tenants = {}  # tenant_id -> {quota, used, data}

    def create_tenant(self, tenant_id, quota=1000):
        self._tenants[tenant_id] = {"quota": quota, "used": 0, "data": {}}

    def store(self, tenant_id, key, value, size=1):
        tenant = self._tenants.get(tenant_id)
        if tenant is None:
            raise KeyError(f"Unknown tenant: {tenant_id}")
        tenant["data"][key] = value
        tenant["used"] += size
        if tenant["used"] > tenant["quota"]:  # BUG 1: check should happen BEFORE storing
            raise RuntimeError("Quota exceeded")

    def retrieve(self, tenant_id, key):
        tenant = self._tenants.get(tenant_id)
        if tenant is None:
            raise KeyError(f"Unknown tenant: {tenant_id}")
        return tenant["data"].get(key)

    def list_keys(self, tenant_id):
        # BUG 2: should only return keys for the given tenant
        all_keys = []
        for t in self._tenants.values():
            all_keys.extend(t["data"].keys())
        return all_keys
