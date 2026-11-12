# Mission 001 - Hello Status Banner
# Builds the SSH login banner for a server.
def banner(host, port):
    return "Host " + host + " is listening on port " + port


def replica_line(service, replicas):
    return service + " is running " + replicas + " replicas"


def full_banner(host, port, service, replicas):
    lines = [banner(host, port), replica_line(service, replicas)]
    return "\n".join(lines)


if __name__ == "__main__":
    print(full_banner("lf-edge-07", 8080, "router", 3))
