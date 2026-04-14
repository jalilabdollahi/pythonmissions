# Mission 074 - Solution
from collections import defaultdict

def group_by_region(servers):
    groups = defaultdict(list)
    for s in servers:
        groups[s["region"]].append(s["name"])
    return dict(groups)

if __name__ == "__main__":
    svrs = [
        {"name": "web-01", "region": "us-east"},
        {"name": "web-02", "region": "eu-west"},
        {"name": "web-03", "region": "us-east"},
    ]
    print(group_by_region(svrs))
