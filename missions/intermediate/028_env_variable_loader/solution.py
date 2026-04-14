# Mission 028 - Environment Variable Loader
# Fixed solution
import os

def load_env(key, default=None, cast=None):
    value = os.environ.get(key)
    if value is None:
        return default
    if cast:
        return cast(value)
    return value

def get_port(default=8080):
    return load_env("PORT", default=default, cast=int)
