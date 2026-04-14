# Mission 029 (Advanced) - Multi-Tenant Isolation
# Fixed solution

class TenantManager:
    def __init__(self):
        self._tenants = {}

    def create_tenant(self, tenant_id, quota=1000):
        self._tenants[tenant_id] = {"quota": quota, "used": 0, "data": {}}

    def store(self, tenant_id, key, value, size=1):
        tenant = self._tenants.get(tenant_id)
        if tenant is None:
            raise KeyError(f"Unknown tenant: {tenant_id}")
        if tenant["used"] + size > tenant["quota"]:
            raise RuntimeError("Quota exceeded")
        tenant["data"][key] = value
        tenant["used"] += size

    def retrieve(self, tenant_id, key):
        tenant = self._tenants.get(tenant_id)
        if tenant is None:
            raise KeyError(f"Unknown tenant: {tenant_id}")
        return tenant["data"].get(key)

    def list_keys(self, tenant_id):
        tenant = self._tenants.get(tenant_id)
        if tenant is None:
            raise KeyError(f"Unknown tenant: {tenant_id}")
        return list(tenant["data"].keys())
