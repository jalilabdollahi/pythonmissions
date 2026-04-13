# Mission 10 - Load YAML Config
# Fix the 2 bugs in this script.

import yaml


def load_yaml_config(filepath):
    with open(filepath, "r") as f:
        return yaml.load(f)


def get_db_settings(config):
    return {
        "host": config["database"]["host"],
        "port": config["database"].get("port", 5432),
        "name": config["database"].get("name", "appdb"),
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
