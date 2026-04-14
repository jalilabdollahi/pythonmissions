# Mission 040 - Check for Required Keys
# Fix the bug.

def has_required_keys(cfg, required):
    """Return True if all required keys exist in cfg."""
    return all(required)

if __name__ == "__main__":
    cfg = {"host": "localhost", "port": 5432}
    print(has_required_keys(cfg, ["host", "port", "db_name"]))
