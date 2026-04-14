# Mission 077 - Shared vs Per-Instance Config
class Connection:
    timeout = 30

    def __init__(self, host, timeout):
        self.host = host

    def describe(self):
        return f"{self.host} timeout={self.timeout}"

if __name__ == "__main__":
    c1 = Connection("db-01", 10)
    c2 = Connection("db-02", 60)
    print(c1.describe())
    print(c2.describe())
