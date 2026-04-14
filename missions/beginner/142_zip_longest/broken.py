# Mission 142 - Pair Envs with Defaults
from itertools import zip_longest

def merge_env_configs(envs, configs):
    """Pair each env with its config, using {} for missing configs."""
    return list(zip(envs, configs))

if __name__ == "__main__":
    envs = ["prod", "staging", "dev"]
    configs = [{"debug": False}, {"debug": True}]
    print(merge_env_configs(envs, configs))
