# Mission 109 - Health Status Aggregator
# Fix the 2 bugs in this script.

STATUS_SEVERITY = {"healthy": 0, "degraded": 1, "unhealthy": 2}

def aggregate_health(components):
    """Return overall status dict from component statuses."""
    if not components:
        return {"status": "healthy", "components": {}}
    statuses = [c["status"] for c in components.values()]
    worst = min(statuses, key=lambda s: STATUS_SEVERITY.get(s, 0))  # BUG 1: should be max
    details = {}
    for name, comp in components.items():
        details[name] = comp["status"]
    return {"status": worst, "components": details}

def is_healthy(health_response):
    return health_response["status"] == "healthy"

def has_degraded(health_response):
    comps = health_response.get("components", {})
    return "degraded" not in comps.values()  # BUG 2: logic inverted — should be "in"
