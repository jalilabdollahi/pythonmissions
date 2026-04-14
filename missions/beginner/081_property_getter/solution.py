# Mission 081 - Solution
class Service:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    @property
    def endpoint(self):
        return f"{self.host}:{self.port}"

if __name__ == "__main__":
    svc = Service("localhost", 8080)
    print(svc.endpoint)
