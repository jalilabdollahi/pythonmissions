# Mission 082 - Port Collision Detector
# Reverse lookup of host ports to find clashing services.


def by_port(services):
    return {port: name for name, port in services.items()}


def owner_of(services, port):
    for name, p in services.items():
        if p == port:
            return name
    return None


def free_ports(services, candidates):
    used = set(services.values())
    return [p for p in candidates if p not in used]


def check_config(services):
    try:
        by_port(services)
    except ValueError as exc:
        return f"conflict: {exc}"
    return "ok"


if __name__ == "__main__":
    cfg = {"api": 8080, "web": 8081, "metrics": 8080}
    print(check_config(cfg))
    print(free_ports(cfg, [8080, 8082, 8083]))
