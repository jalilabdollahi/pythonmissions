# Mission 125 - Layered Config Merge (solution)
# Merge layered configuration dicts recursively, with None meaning "remove".
import copy


def deep_merge(base, override):
    result = copy.deepcopy(base)
    for key, value in override.items():
        if value is None:
            result.pop(key, None)
        elif isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


def build_config(*layers):
    config = {}
    for layer in layers:
        config = deep_merge(config, layer)
    return config


def flatten(config, prefix=""):
    flat = {}
    for key in sorted(config):
        name = f"{prefix}{key}"
        if isinstance(config[key], dict):
            flat.update(flatten(config[key], name + "."))
        else:
            flat[name] = config[key]
    return flat
