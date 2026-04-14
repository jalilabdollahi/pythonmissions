# Mission 076 - Solution
class Service:
    def __init__(self, name, host, port):
        self.name = name
        self.host = host
        self.port = port

    def endpoint(self):
        return f"{self.host}:{self.port}"

if __name__ == "__main__":
    svc = Service("web", "localhost", 8080)
    print(svc.endpoint())
