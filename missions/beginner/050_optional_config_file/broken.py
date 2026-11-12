# Mission 050 - Missing Optional Settings
# Load optional per-machine overrides on top of built-in defaults.
import json

DEFAULTS = {"timeout": 30, "retries": 3, "region": "eu-west"}


def load_settings(path):
    settings = DEFAULTS
    with open(path, encoding="utf-8") as handle:
        overrides = json.load(handle)
    settings.update(overrides)
    return settings


def describe(settings):
    return ", ".join(f"{key}={settings[key]}" for key in sorted(settings))
