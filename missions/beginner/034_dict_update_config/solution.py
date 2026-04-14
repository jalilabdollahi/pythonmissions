# Mission 034 - Solution

def merge_config(base, override):
    result = dict(base)
    result.update(override)
    return result

if __name__ == "__main__":
    base = {"host": "localhost", "port": 5432, "timeout": 30}
    override = {"port": 5433, "debug": True}
    print(merge_config(base, override))
