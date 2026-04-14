# Mission 039 - Access Nested Config
# Fix the bug.

def safe_get(cfg, *keys):
    """Traverse nested dict by keys, return value or None if any key missing."""
    current = cfg
    for key in keys:
        current = current[key]
    return current

if __name__ == "__main__":
    cfg = {"database": {"host": "db.internal", "port": 5432}}
    print(safe_get(cfg, "database", "host"))
    print(safe_get(cfg, "database", "password"))
