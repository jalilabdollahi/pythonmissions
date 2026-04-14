# Mission 072 - Pretty-Print the Config
import json

def pretty_json(data):
    """Return data serialized as indented JSON string."""
    return json.dumps(data)

if __name__ == "__main__":
    cfg = {"host": "localhost", "port": 5432, "debug": True}
    print(pretty_json(cfg))
