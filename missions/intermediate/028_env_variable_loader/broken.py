# Mission 028 - Environment Variable Loader
# Fix the 2 bugs in this script.
import os

def load_env(key, default=None, cast=None):
    value = os.environ[key]  # BUG 1: raises KeyError if not set — use .get()
    if value is None:
        return default
    if cast:
        return cast(value)
    return value

def get_port(default=8080):
    return load_env("PORT", default=default, cast=str)  # BUG 2: should cast to int
