# Mission 080 - Solution
class Service:
    def __init__(self, name, host, port):
        self.name = name
        self.host = host
        self.port = port

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["host"], data["port"])

if __name__ == "__main__":
    svc = Service.from_dict({"name": "web", "host": "localhost", "port": 8080})
    print(svc.name, svc.port)
