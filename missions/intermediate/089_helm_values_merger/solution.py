# Mission 089 - Helm Values Merger
# Fixed solution
import copy

def merge_helm_values(base, override):
    result = copy.deepcopy(base)
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_helm_values(result[key], value)
        else:
            result[key] = value
    return result

def apply_env_values(base_values, env_values, env):
    merged = merge_helm_values(base_values, env_values.get(env, {}))
    merged["deployedEnv"] = env
    return merged
