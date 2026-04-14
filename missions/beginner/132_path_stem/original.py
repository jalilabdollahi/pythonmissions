# Mission 132 - Extract Config Name
from pathlib import Path

def get_config_name(filepath):
    """Return filename without extension."""
    path = Path(filepath)
    return path.name

if __name__ == "__main__":
    print(get_config_name("/etc/myapp/database.yaml"))
