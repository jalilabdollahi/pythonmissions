# Mission 082 - Compare Two Configs
class Config:
    def __init__(self, data):
        self.data = data

if __name__ == "__main__":
    c1 = Config({"host": "localhost", "port": 5432})
    c2 = Config({"host": "localhost", "port": 5432})
    print(c1 == c2)
