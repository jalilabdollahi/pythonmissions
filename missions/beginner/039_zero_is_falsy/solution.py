# Mission 039 - Zero Replicas Ignored (solution)
# Resolve scaling settings while honouring deliberate zeros.


def resolve_replicas(requested, default=2):
    if requested is None:
        return default
    return requested


def resolve_canary_percent(config):
    percent = config.get("canary_percent")
    if percent is None:
        return 10
    return percent


def plan(apps):
    return {name: resolve_replicas(spec.get("replicas")) for name, spec in apps.items()}
