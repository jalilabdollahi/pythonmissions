# Mission 024 - Property Validation
# Fix the 2 bugs in this script.

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port  # uses setter

    @property
    def port(self):
        return self._port

    @port.setters  # BUG 1: should be @port.setter (no 's')
    def port(self, value):
        if value < 0 or value > 65535:  # BUG 2: should be value < 1
            raise ValueError(f"Invalid port: {value}")
        self._port = value

    def address(self):
        return f"{self.host}:{self._port}"
