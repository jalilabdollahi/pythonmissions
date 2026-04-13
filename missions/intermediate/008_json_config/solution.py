# Mission 08 - Solution

import json
import os


def load_config(filepath):
    if not os.path.exists(filepath):
        return {}
    with open(filepath, "r") as f:
        return json.load(f)


def save_config(filepath, config):
    with open(filepath, "w") as f:
        json.dump(config, f, indent=2)


def update_config(filepath, updates):
    config = load_config(filepath)
    config.update(updates)
    save_config(filepath, config)
    return config


if __name__ == "__main__":
    path = "/tmp/app_config.json"
    save_config(path, {"env": "staging", "debug": False, "replicas": 3})
    cfg = load_config(path)
    print(f"Loaded config: {cfg}")
    update_config(path, {"replicas": 5})
    print(f"Updated config: {load_config(path)}")
