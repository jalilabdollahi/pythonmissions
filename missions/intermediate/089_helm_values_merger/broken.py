# Mission 089 - Helm Values Merger
# Fix the 2 bugs in this script.
import copy

def merge_helm_values(base, override):
    """Deep merge override into base. Override wins on conflicts."""
    result = base  # BUG 1: should copy.deepcopy(base) — mutates original
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_helm_values(result[key], value)
        else:
            result[key] = value
    return result

def apply_env_values(base_values, env_values, env):
    """Apply environment-specific overrides."""
    merged = merge_helm_values(base_values, env_values.get(env, {}))
    merged["deployedEnv"] = env
    return merged
