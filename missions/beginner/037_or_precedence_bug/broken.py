# Mission 037 - Always Healthy Dashboard
# Decide which services count as healthy for the status page.


def is_acceptable(status):
    return status == "ok" or "warn"


def healthy_services(statuses):
    return sorted(name for name, status in statuses.items() if is_acceptable(status))


def status_banner(statuses):
    bad = len(statuses) - len(healthy_services(statuses))
    return "All systems operational" if bad == 0 else f"{bad} service(s) degraded"
