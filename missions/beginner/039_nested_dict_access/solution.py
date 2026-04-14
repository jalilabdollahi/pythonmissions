# Mission 039 - Solution

def safe_get(cfg, *keys):
    current = cfg
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current

if __name__ == "__main__":
    cfg = {"database": {"host": "db.internal", "port": 5432}}
    print(safe_get(cfg, "database", "host"))
    print(safe_get(cfg, "database", "password"))
