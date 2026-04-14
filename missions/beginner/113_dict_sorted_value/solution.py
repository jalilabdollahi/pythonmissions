# Mission 113 - Solution
def sorted_config(cfg):
    return sorted(cfg.items(), key=lambda kv: kv[0])

if __name__ == "__main__":
    cfg = {"port": "5432", "host": "localhost", "db": "myapp"}
    for k, v in sorted_config(cfg):
        print(f"{k}={v}")
