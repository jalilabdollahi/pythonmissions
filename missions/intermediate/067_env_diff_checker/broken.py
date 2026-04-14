# Mission 067 - Environment Diff Checker
# Fix the 2 bugs in this script.

def diff_envs(env_a, env_b):
    """Return dict of differences between two environment configs."""
    diffs = {}
    all_keys = set(env_a.keys()) | set(env_b.keys())
    for key in all_keys:
        a_val = env_a.get(key)
        b_val = env_b.get(key)
        if a_val == b_val:
            diffs[key] = {"a": a_val, "b": b_val}  # BUG 1: should only add when different
    return diffs

def has_drift(env_a, env_b):
    return diff_envs(env_a, env_b) != {}  # this is fine actually

def critical_drift(env_a, env_b, critical_keys):
    diffs = diff_envs(env_a, env_b)
    return [k for k in critical_keys if k in diffs]  # BUG 2: this is fine IF bug 1 is fixed; redundant check
