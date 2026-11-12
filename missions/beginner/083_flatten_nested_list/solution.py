# Mission 083 - Flatten the Subnets (solution)
# Turns per-subnet reservations into flat address lists.


def all_ips(subnets):
    return [ip for subnet in subnets for ip in subnet["ips"]]


def ip_count(subnets):
    return len(all_ips(subnets))


def ips_for_firewall(subnets):
    return [f"allow {ip}" for ip in all_ips(subnets)]


def cidrs_with_ips(subnets):
    return [s["cidr"] for s in subnets if s["ips"]]


def busiest_subnet(subnets):
    if not subnets:
        return None
    return max(subnets, key=lambda s: len(s["ips"]))["cidr"]


if __name__ == "__main__":
    plan = [
        {"cidr": "10.0.1.0/24", "ips": ["10.0.1.5", "10.0.1.9"]},
        {"cidr": "10.0.2.0/24", "ips": []},
        {"cidr": "10.0.3.0/24", "ips": ["10.0.3.4"]},
    ]
    print(ips_for_firewall(plan))
