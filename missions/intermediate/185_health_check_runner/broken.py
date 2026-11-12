# Mission 185 - Probe Parade
# Run HTTP health checks through an injected fetch function and map outcomes to states.
DEFAULT_TIMEOUT = 2.0


def classify_status(status):
    if 200 <= status < 400:
        return "up"
    if 500 <= status < 600:
        return "down"
    return "degraded"


def run_check(check, fetch):
    timeout = DEFAULT_TIMEOUT
    try:
        status = fetch(check["url"], timeout)
        state = classify_status(status)
    except OSError:
        state = "unreachable"
    except TimeoutError:
        state = "timeout"
    return {"name": check["name"], "state": state}


def run_all(checks, fetch):
    return [run_check(check, fetch) for check in checks]


def overall(results):
    states = {r["state"] for r in results}
    if states <= {"up"}:
        return "ok"
    if states & {"down", "timeout", "unreachable"}:
        return "critical"
    return "warning"
