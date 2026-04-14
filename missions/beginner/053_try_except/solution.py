# Mission 053 - Solution
import json

def load_config(path):
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

if __name__ == "__main__":
    print(load_config("/tmp/nonexistent.json"))
