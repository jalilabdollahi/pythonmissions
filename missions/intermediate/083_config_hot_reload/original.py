# Mission 083 - Config Hot Reload
# Fix the 2 bugs in this script.
import json
import os

class HotConfig:
    def __init__(self, path):
        self.path = path
        self._config = {}
        self._mtime = 0

    def _load(self):
        with open(self.path) as f:
            self._config = json.load(f)
        self._mtime = os.path.getmtime(self.path)

    def _needs_reload(self):
        current_mtime = os.path.getmtime(self.path)
        return current_mtime != self._mtime  # this is correct

    def get(self, key, default=None):
        self._load()  # BUG 1: should only reload if _needs_reload()
        return self._config.get(key, default)

    def reload_if_changed(self):
        if self._needs_reload():
            self._load()
            return True
        return False  # BUG 2: this is correct — bug was in get()
