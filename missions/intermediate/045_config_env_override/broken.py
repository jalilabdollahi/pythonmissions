# Mission 045 - Config with Env Override
# Fix the 2 bugs in this script.
import os

DEFAULTS = {
    "PORT": 8080,
    "HOST": "0.0.0.0",
    "DEBUG": False,
    "WORKERS": 4,
}

def load_with_env_override(defaults=None):
    config = dict(defaults or DEFAULTS)
    for key, default_val in defaults.items() if defaults else DEFAULTS.items():
        env_val = os.environ.get(key)
        if env_val is not None:
            # Cast to same type as default
            target_type = type(default_val)
            if target_type == bool:
                config[key] = env_val.lower() in ("1", "true", "yes")
            else:
                config[key] = target_type(env_val)
    return config

def get_workers():
    cfg = load_with_env_override()
    workers = cfg.get("WORKERS")
    return workers + "1"  # BUG: should be workers + 1 (not string concat)
