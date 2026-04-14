# Mission 128 - Generate Config Lines
def config_stream(cfg):
    """Yield 'key=value' lines from config dict one at a time."""
    return [f"{k}={v}" for k, v in cfg.items()]

if __name__ == "__main__":
    import types
    cfg = {"host": "localhost", "port": "5432", "db": "myapp"}
    stream = config_stream(cfg)
    print(type(stream))
    for line in stream:
        print(line)
