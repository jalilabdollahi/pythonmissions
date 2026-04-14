# Mission 067 - Environment Diff Checker
# Fixed solution

def diff_envs(env_a, env_b):
    diffs = {}
    all_keys = set(env_a.keys()) | set(env_b.keys())
    for key in all_keys:
        a_val = env_a.get(key)
        b_val = env_b.get(key)
        if a_val != b_val:
            diffs[key] = {"a": a_val, "b": b_val}
    return diffs

def has_drift(env_a, env_b):
    return diff_envs(env_a, env_b) != {}

def critical_drift(env_a, env_b, critical_keys):
    diffs = diff_envs(env_a, env_b)
    return [k for k in critical_keys if k in diffs]
