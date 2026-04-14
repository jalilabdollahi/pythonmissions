# Mission 022 - Config Dictionary Merge
# Fixed solution

def merge_configs(base, override):
    """Merge override into base config, override wins."""
    result = base.copy()
    result.update(override)
    return result

def deep_merge(base, override):
    """Deep merge: nested dicts are merged recursively."""
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result
