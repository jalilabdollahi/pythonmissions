# Mission 143 - Solution
from itertools import groupby

def group_by_service(deployments):
    result = {}
    key = lambda d: d["service"]
    for svc, group in groupby(sorted(deployments, key=key), key=key):
        result[svc] = list(group)
    return result

if __name__ == "__main__":
    deps = [
        {"service":"web","version":"1.2"},
        {"service":"api","version":"2.0"},
        {"service":"web","version":"1.3"},
    ]
    print(group_by_service(deps))
