# Mission 040 - Solution

def has_required_keys(cfg, required):
    return all(k in cfg for k in required)

if __name__ == "__main__":
    cfg = {"host": "localhost", "port": 5432}
    print(has_required_keys(cfg, ["host", "port", "db_name"]))
