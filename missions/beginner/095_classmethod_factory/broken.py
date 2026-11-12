# Mission 095 - Parsing Servers From Strings
# Builds server objects from host:port strings in legacy sheets.


class Server:
    scheme = "http"

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def from_string(cls, text):
        host, port = text.strip().rsplit(":", 1)
        return Server(host, int(port))

    def url(self):
        return f"{self.scheme}://{self.host}:{self.port}"


class TlsServer(Server):
    scheme = "https"


def load_all(cls, lines):
    return [cls.from_string(line) for line in lines if line.strip()]


if __name__ == "__main__":
    for s in load_all(TlsServer, ["web:443", "api:8443"]):
        print(s.url())
