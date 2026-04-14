# Mission 074 - Group Servers by Region
from collections import defaultdict

def group_by_region(servers):
    """Return dict grouping server names by region."""
    groups = dict()
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
