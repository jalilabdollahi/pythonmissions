# Mission 154 - Borrowed Environment (solution)
# Context managers that temporarily change process state and put it back.
import os
from contextlib import contextmanager


def _restore(env, saved):
    for key, old in saved.items():
        if old is None:
            env.pop(key, None)
        else:
            env[key] = old


@contextmanager
def temporary_env(env, **overrides):
    saved = {key: env.get(key) for key in overrides}
    env.update(overrides)
    try:
        yield env
    finally:
        _restore(env, saved)


@contextmanager
def working_directory(path):
    previous = os.getcwd()
    os.chdir(path)
    try:
        yield os.getcwd()
    finally:
        os.chdir(previous)


def describe(env):
    region = env.get("REGION", "unset")
    debug = env.get("DEBUG", "0")
    return f"region={region} debug={debug}"
