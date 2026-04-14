# Mission 037 - Loop the Config Items
# Fix the bug.

def print_config(cfg):
    """Print each config entry as 'key=value'."""
    lines = []
    for key, value in cfg:
        lines.append(f"{key}={value}")
    return lines

if __name__ == "__main__":
    config = {"host": "localhost", "port": "5432", "db": "myapp"}
    for line in print_config(config):
        print(line)
