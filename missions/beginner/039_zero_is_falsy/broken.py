# Mission 039 - Zero Replicas Ignored
# Resolve scaling settings while honouring deliberate zeros.


def resolve_replicas(requested, default=2):
    if not requested:
        return default
    return requested


def resolve_canary_percent(config):
    percent = config.get("canary_percent")
    if not percent:
        return 10
    return percent


def plan(apps):
    return {name: resolve_replicas(spec.get("replicas")) for name, spec in apps.items()}
