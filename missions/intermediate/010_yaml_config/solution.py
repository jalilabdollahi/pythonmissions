# Mission 10 - Solution

import yaml


def load_yaml_config(filepath):
    with open(filepath, "r") as f:
        return yaml.safe_load(f)


def get_db_settings(config):
    db = config.get("database", {})
    return {
        "host": db.get("host", "localhost"),
        "port": db.get("port", 5432),
        "name": db.get("name", "appdb"),
    }


def get_service_settings(config):
    service = config.get("service", {})
    return {
        "name": service.get("name", "unknown"),
        "port": service.get("port", 8080),
        "debug": service.get("debug", False),
    }


if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "config.yaml"
    config = load_yaml_config(path)
    print("DB:", get_db_settings(config))
    print("Service:", get_service_settings(config))
