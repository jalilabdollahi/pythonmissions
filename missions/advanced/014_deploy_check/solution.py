# Mission 14 - Solution


def is_newer_version(new_version, current_version):
    def parse(v):
        return tuple(int(x) for x in v.split("."))

    return parse(new_version) > parse(current_version)


def is_healthy_enough(replicas, min_healthy=0.8):
    if not replicas:
        return False

    healthy_replicas = [r for r in replicas if r["healthy"]]
    fraction = len(healthy_replicas) / len(replicas)

    return fraction >= min_healthy


def can_deploy(new_version, current_version, replicas, min_healthy=0.8):
    if not is_newer_version(new_version, current_version):
        return False, f"Version {new_version} is not newer than {current_version}"

    if not is_healthy_enough(replicas, min_healthy):
        healthy = sum(1 for r in replicas if r["healthy"])
        return False, f"Only {healthy}/{len(replicas)} replicas healthy (need {min_healthy:.0%})"

    return True, f"All checks passed - deploying {new_version}"


if __name__ == "__main__":
    replicas = [
        {"id": "pod-1", "healthy": True},
        {"id": "pod-2", "healthy": True},
        {"id": "pod-3", "healthy": False},
        {"id": "pod-4", "healthy": True},
    ]
    allowed, reason = can_deploy("2.1.0", "2.0.9", replicas)
    print(f"Deploy allowed: {allowed} - {reason}")
