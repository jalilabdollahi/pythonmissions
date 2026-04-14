# Mission 016 - JSON Config Loader
# Fixed solution
import json

def load_config(filepath):
    with open(filepath, "r") as f:
        content = f.read()
    config = json.loads(content)
    return config

def get_setting(config, key, default=None):
    return config.get(key, default)
