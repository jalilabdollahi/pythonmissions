# Mission 109 - Health Status Aggregator
# Fixed solution

STATUS_SEVERITY = {"healthy": 0, "degraded": 1, "unhealthy": 2}

def aggregate_health(components):
    if not components:
        return {"status": "healthy", "components": {}}
    statuses = [c["status"] for c in components.values()]
    worst = max(statuses, key=lambda s: STATUS_SEVERITY.get(s, 0))
    details = {}
    for name, comp in components.items():
        details[name] = comp["status"]
    return {"status": worst, "components": details}

def is_healthy(health_response):
    return health_response["status"] == "healthy"

def has_degraded(health_response):
    comps = health_response.get("components", {})
    return "degraded" in comps.values()
