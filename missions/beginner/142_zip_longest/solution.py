# Mission 142 - Solution
from itertools import zip_longest

def merge_env_configs(envs, configs):
    return list(zip_longest(envs, configs, fillvalue={}))

if __name__ == "__main__":
    envs = ["prod", "staging", "dev"]
    configs = [{"debug": False}, {"debug": True}]
    print(merge_env_configs(envs, configs))
