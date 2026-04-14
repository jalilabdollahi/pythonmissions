# Mission 132 - Solution
from pathlib import Path

def get_config_name(filepath):
    path = Path(filepath)
    return path.stem

if __name__ == "__main__":
    print(get_config_name("/etc/myapp/database.yaml"))
