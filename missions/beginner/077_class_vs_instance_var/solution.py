# Mission 077 - Solution
class Connection:
    def __init__(self, host, timeout):
        self.host = host
        self.timeout = timeout

    def describe(self):
        return f"{self.host} timeout={self.timeout}"

if __name__ == "__main__":
    c1 = Connection("db-01", 10)
    c2 = Connection("db-02", 60)
    print(c1.describe())
    print(c2.describe())
