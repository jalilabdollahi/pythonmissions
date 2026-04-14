# Mission 128 - Solution
def config_stream(cfg):
    for k, v in cfg.items():
        yield f"{k}={v}"

if __name__ == "__main__":
    import types
    cfg = {"host": "localhost", "port": "5432", "db": "myapp"}
    stream = config_stream(cfg)
    print(type(stream))
    for line in stream:
        print(line)
