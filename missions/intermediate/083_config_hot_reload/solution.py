# Mission 083 - Config Hot Reload
# Fixed solution
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
        return current_mtime != self._mtime

    def get(self, key, default=None):
        if self._needs_reload():
            self._load()
        return self._config.get(key, default)

    def reload_if_changed(self):
        if self._needs_reload():
            self._load()
            return True
        return False
