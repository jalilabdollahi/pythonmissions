# Mission 016 - JSON Config Loader
# Fix the 2 bugs in this script.
import json

def load_config(filepath):
    with open(filepath, "r") as f:
        content = f.read()
    config = json.loads(f)  # BUG 1: should be json.loads(content) or json.load(open(...))
    return config

def get_setting(config, key, default=None):
    return config[key]  # BUG 2: should use .get() to support default
