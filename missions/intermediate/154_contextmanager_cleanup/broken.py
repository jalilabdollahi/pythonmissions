# Mission 154 - Borrowed Environment
# Context managers that temporarily change process state and put it back.
import os
from contextlib import contextmanager


def _restore(env, saved):
    for key, old in saved.items():
        env[key] = old


@contextmanager
def temporary_env(env, **overrides):
    saved = {key: env.get(key) for key in overrides}
    env.update(overrides)
    yield env
    _restore(env, saved)


@contextmanager
def working_directory(path):
    os.chdir(path)
    previous = os.getcwd()
    try:
        yield os.getcwd()
    finally:
        os.chdir(previous)


def describe(env):
    region = env.get("REGION", "unset")
    debug = env.get("DEBUG", "0")
    return f"region={region} debug={debug}"
