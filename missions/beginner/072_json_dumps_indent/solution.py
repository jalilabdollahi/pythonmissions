# Mission 072 - Solution
import json

def pretty_json(data):
    return json.dumps(data, indent=2)

if __name__ == "__main__":
    cfg = {"host": "localhost", "port": 5432, "debug": True}
    print(pretty_json(cfg))
