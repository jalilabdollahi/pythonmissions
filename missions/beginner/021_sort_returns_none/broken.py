# Mission 021 - Failover Order Is None
# Computes the order in which standby hosts are tried.
def failover_order(hosts):
    ordered = hosts.sort()
    return ordered


def first_standby(hosts):
    order = failover_order(hosts)
    return order[0] if order else None


def describe(hosts):
    order = failover_order(hosts)
    if not order:
        return "no standbys"
    return "try: " + " -> ".join(order)


if __name__ == "__main__":
    print(describe(["standby-c", "standby-a", "standby-b"]))
