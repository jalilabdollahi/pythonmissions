# Mission 082 - Solution
class Config:
    def __init__(self, data):
        self.data = data

    def __eq__(self, other):
        if not isinstance(other, Config):
            return NotImplemented
        return self.data == other.data

if __name__ == "__main__":
    c1 = Config({"host": "localhost", "port": 5432})
    c2 = Config({"host": "localhost", "port": 5432})
    print(c1 == c2)
