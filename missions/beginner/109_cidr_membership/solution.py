# Mission 109 - Office VPN Gatekeeper (solution)
# Decides whether a client address belongs to one of the allowed office networks.
import ipaddress


def in_subnet(ip, cidr):
    return ipaddress.ip_address(ip) in ipaddress.ip_network(cidr, strict=False)


def is_allowed(ip, cidrs):
    return any(in_subnet(ip, cidr) for cidr in cidrs)


def matching_network(ip, cidrs):
    for cidr in cidrs:
        if in_subnet(ip, cidr):
            return cidr
    return None


def portal_decision(ip, cidrs):
    network = matching_network(ip, cidrs)
    if network is None:
        return f"deny {ip}"
    return f"allow {ip} via {network}"


if __name__ == "__main__":
    OFFICES = ["10.20.0.0/16", "172.16.4.0/24"]
    print(portal_decision("10.20.99.1", OFFICES))
