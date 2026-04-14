# Mission 037 - Solution

def print_config(cfg):
    lines = []
    for key, value in cfg.items():
        lines.append(f"{key}={value}")
    return lines

if __name__ == "__main__":
    config = {"host": "localhost", "port": "5432", "db": "myapp"}
    for line in print_config(config):
        print(line)
