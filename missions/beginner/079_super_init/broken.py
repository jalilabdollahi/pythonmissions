# Mission 079 - Initialize the Subclass
class Service:
    def __init__(self, name, host, port):
        self.name = name
        self.host = host
        self.port = port

class MonitoredService(Service):
    def __init__(self, name, host, port, check_interval=60):
        self.check_interval = check_interval

    def describe(self):
        return f"{self.name} @ {self.host}:{self.port} every {self.check_interval}s"

if __name__ == "__main__":
    svc = MonitoredService("web", "localhost", 8080, 30)
    print(svc.describe())
