# Mission 058 - Solution
import os

def config_path(base_dir, filename):
    return os.path.join(base_dir, filename)

if __name__ == "__main__":
    print(config_path("/etc/myapp", "config.yaml"))
