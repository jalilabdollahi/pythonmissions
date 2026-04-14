# Mission 146 - Solution
def merge(base, override):
    return base | override

if __name__ == "__main__":
    b = {"host": "localhost", "port": 5432}
    o = {"port": 5433, "debug": True}
    result = merge(b, o)
    print("base:", b)
    print("result:", result)
