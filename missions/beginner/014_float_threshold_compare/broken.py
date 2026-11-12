# Mission 014 - Penny Drift
# Reconciles measured disk usage with invoiced usage.
import math


def total_usage(volumes):
    return sum(volumes)


def matches_invoice(volumes, invoiced):
    return total_usage(volumes) == invoiced


def mismatches(customers):
    bad = []
    for name, (volumes, invoiced) in customers.items():
        if not matches_invoice(volumes, invoiced):
            bad.append(name)
    return sorted(bad)


if __name__ == "__main__":
    print(mismatches({"acme": ([0.1, 0.2], 0.3)}), math.pi)
