# Mission 085 - Hosts by Region
# Groups inventory hosts by region for the capacity review.
from collections import defaultdict


def group_by_region(hosts):
    groups = {}
    for hostname, region in hosts:
        groups[region].append(hostname)
    return dict(groups)


def region_sizes(hosts):
    return {region: len(names) for region, names in group_by_region(hosts).items()}


def largest_region(hosts):
    sizes = region_sizes(hosts)
    if not sizes:
        return None
    return max(sizes, key=sizes.get)


def report(hosts):
    groups = group_by_region(hosts)
    return [f"{region}: {', '.join(groups[region])}" for region in sorted(groups)]


if __name__ == "__main__":
    inventory = [("a1", "eu-west"), ("b1", "us-east"), ("a2", "eu-west")]
    print("\n".join(report(inventory)))
