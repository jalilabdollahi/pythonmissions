# Mission 162 - Safe Config Swap
# Replace a config file atomically so readers never see a half-written version.
import json
import os
import tempfile


def _write_temp(fd, text):
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(text)
        handle.flush()


def atomic_write_text(path, text):
    path = os.fspath(path)
    fd, tmp = tempfile.mkstemp(prefix=".tmp-")
    _write_temp(fd, text)
    os.replace(tmp, path)
    return path


def update_config(path, updates):
    try:
        with open(path, encoding="utf-8") as handle:
            current = json.load(handle)
    except FileNotFoundError:
        current = {}
    current.update(updates)
    atomic_write_text(path, json.dumps(current, indent=2, sort_keys=True))
    return current
