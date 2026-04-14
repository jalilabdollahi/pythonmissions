# Mission 053 - Handle the Missing File
import json

def load_config(path):
    """Return config dict from JSON file, or {} if file not found."""
    with open(path) as f:
        return json.load(f)

if __name__ == "__main__":
    print(load_config("/tmp/nonexistent.json"))
