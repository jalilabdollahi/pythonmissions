# Mission 058 - Join Config Path
import os

def config_path(base_dir, filename):
    """Return path joining base_dir and filename safely."""
    return base_dir + "/" + filename

if __name__ == "__main__":
    print(config_path("/etc/myapp", "config.yaml"))
