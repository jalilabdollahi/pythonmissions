# Mission 018 - Firewall Rule Builder
# Generates firewall allow rules from integer ports.
def port_list(ports):
    return ",".join(ports)


def allow_rule(proto, ports):
    return f"allow {proto} {port_list(ports)}"


def rules_for(services):
    return [allow_rule(proto, ports) for _, (proto, ports) in sorted(services.items())]


if __name__ == "__main__":
    print(rules_for({"web": ("tcp", [80, 443]), "dns": ("udp", [53])}))
