# Mission 070 - Ports From Outer Space
# Validates port numbers typed into the firewall request form.

MAX_PORT = 65535


def validate_port(text):
    port = int(text)
    if port > MAX_PORT:
        raise ValueError("port out of range: %d" % port)
    return port


def parse_port_list(text):
    return [validate_port(part.strip()) for part in text.split(",")]


def open_rules(text):
    return ["allow tcp %d" % port for port in parse_port_list(text)]


def is_privileged(port):
    return port < 1024


def split_privileged(text):
    ports = parse_port_list(text)
    return (
        [p for p in ports if is_privileged(p)],
        [p for p in ports if not is_privileged(p)],
    )


if __name__ == "__main__":
    print(open_rules("80,443"))
