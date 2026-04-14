# Mission 033 - Solution

def get_config(cfg, key, default=None):
    return cfg.get(key, default)

if __name__ == "__main__":
    config = {"host": "localhost", "port": 5432}
    print(get_config(config, "host", "unknown"))
    print(get_config(config, "timeout", 30))
