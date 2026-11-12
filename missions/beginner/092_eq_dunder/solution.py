# Mission 092 - Duplicate Endpoint Check (solution)
# Service registry entries with value-based equality.


class Endpoint:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def __eq__(self, other):
        if not isinstance(other, Endpoint):
            return NotImplemented
        return (self.host, self.port) == (other.host, other.port)

    def __hash__(self):
        return hash((self.host, self.port))

    def __repr__(self):
        return f"Endpoint({self.host!r}, {self.port!r})"


def register(registry, endpoint):
    if endpoint in registry:
        return False
    registry.append(endpoint)
    return True


def unique(endpoints):
    result = []
    for endpoint in endpoints:
        register(result, endpoint)
    return result


if __name__ == "__main__":
    reg = []
    print(register(reg, Endpoint("10.0.0.5", 443)))
    print(register(reg, Endpoint("10.0.0.5", 443)))
