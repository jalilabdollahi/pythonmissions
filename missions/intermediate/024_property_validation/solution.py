# Mission 024 - Property Validation
# Fixed solution

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, value):
        if value < 1 or value > 65535:
            raise ValueError(f"Invalid port: {value}")
        self._port = value

    def address(self):
        return f"{self.host}:{self._port}"
