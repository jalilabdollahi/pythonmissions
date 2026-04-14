# Mission 033 - Get Config with Default
# Fix the bug.

def get_config(cfg, key, default=None):
    """Return cfg[key] or default if key is missing."""
    return cfg[key]

if __name__ == "__main__":
    config = {"host": "localhost", "port": 5432}
    print(get_config(config, "host", "unknown"))
    print(get_config(config, "timeout", 30))
