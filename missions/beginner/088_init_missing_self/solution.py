# Mission 088 - Server Object Forgets Everything (solution)
# A tiny model of a provisioned server.


class Server:
    def __init__(self, host, port, role="web"):
        self.host = host
        self.port = port
        self.role = role

    def address(self):
        return f"{self.host}:{self.port}"

    def is_database(self):
        return self.role == "db"

    def describe(self):
        return f"{self.role} server at {self.address()}"


def databases(servers):
    return [s for s in servers if s.is_database()]


def addresses(servers):
    return sorted(s.address() for s in servers)


if __name__ == "__main__":
    fleet = [Server("web-1", 80), Server("pg-1", 5432, role="db")]
    for server in fleet:
        print(server.describe())
