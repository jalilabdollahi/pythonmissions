# Mission 143 - Group Deployments by Service
from itertools import groupby

def group_by_service(deployments):
    """Return {service: [deployment, ...]} dict grouped by service."""
    result = {}
    for svc, group in groupby(deployments, key=lambda d: d["service"]):
        result[svc] = list(group)
    return result

if __name__ == "__main__":
    deps = [
        {"service":"web","version":"1.2"},
        {"service":"api","version":"2.0"},
        {"service":"web","version":"1.3"},
    ]
    print(group_by_service(deps))
