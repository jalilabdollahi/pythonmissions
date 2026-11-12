# Mission 024 - Listening Ports Report
# Reports which service listens on which port.
def listening_lines(ports):
    lines = []
    for service, port in sorted(ports):
        lines.append(f"{service}:{port}")
    return lines


def services_on_port(ports, wanted):
    return sorted(service for service, port in ports.items() if port == wanted)


def highest_port(ports):
    if not ports:
        return None
    return max(ports.items(), key=lambda pair: pair[1])


if __name__ == "__main__":
    print(listening_lines({"ssh": 22, "http": 80, "metrics": 9100}))
