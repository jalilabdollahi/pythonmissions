# Mission 113 - Sort Config by Key
def sorted_config(cfg):
    """Return (key, value) list sorted alphabetically by key."""
    return sorted(cfg.items(), key=lambda kv: kv[1])

if __name__ == "__main__":
    cfg = {"port": "5432", "host": "localhost", "db": "myapp"}
    for k, v in sorted_config(cfg):
        print(f"{k}={v}")
