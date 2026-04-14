# Mission 022 - Config Dictionary Merge
# Fix the 2 bugs in this script.

def merge_configs(base, override):
    """Merge override into base config, override wins."""
    result = base.copy()
    result = result.update(override)  # BUG 1: .update() returns None
    return result

def deep_merge(base, override):
    """Deep merge: nested dicts are merged recursively."""
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = value  # BUG 2: should deep_merge recursively
        else:
            result[key] = value
    return result
