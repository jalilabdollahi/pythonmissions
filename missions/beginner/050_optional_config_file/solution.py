# Mission 050 - Missing Optional Settings (solution)
# Load optional per-machine overrides on top of built-in defaults.
import json

DEFAULTS = {"timeout": 30, "retries": 3, "region": "eu-west"}


def load_settings(path):
    settings = dict(DEFAULTS)
    try:
        with open(path, encoding="utf-8") as handle:
            overrides = json.load(handle)
    except FileNotFoundError:
        return settings
    settings.update(overrides)
    return settings


def describe(settings):
    return ", ".join(f"{key}={settings[key]}" for key in sorted(settings))
