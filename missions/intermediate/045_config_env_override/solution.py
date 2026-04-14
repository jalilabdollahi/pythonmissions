# Mission 045 - Config with Env Override
# Fixed solution
import os

DEFAULTS = {
    "PORT": 8080,
    "HOST": "0.0.0.0",
    "DEBUG": False,
    "WORKERS": 4,
}

def load_with_env_override(defaults=None):
    base = defaults or DEFAULTS
    config = dict(base)
    for key, default_val in base.items():
        env_val = os.environ.get(key)
        if env_val is not None:
            target_type = type(default_val)
            if target_type == bool:
                config[key] = env_val.lower() in ("1", "true", "yes")
            else:
                config[key] = target_type(env_val)
    return config

def get_workers():
    cfg = load_with_env_override()
    workers = cfg.get("WORKERS")
    return workers + 1
