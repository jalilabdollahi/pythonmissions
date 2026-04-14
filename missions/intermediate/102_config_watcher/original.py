# Mission 102 - Config Watcher
# Fix the 2 bugs in this script.
import os

class ConfigWatcher:
    def __init__(self, watch_dir):
        self.watch_dir = os.path.dirname(watch_dir)  # BUG 1: should be abspath, not dirname
        self._callbacks = []
        self._known_files = {}

    def on_change(self, callback):
        self._callbacks.append(callback)

    def _scan(self):
        changed = []
        try:
            for fname in os.listdir(self.watch_dir):
                fpath = os.path.join(self.watch_dir, fname)
                mtime = os.path.getmtime(fpath)
                if fpath not in self._known_files or self._known_files[fpath] != mtime:
                    self._known_files[fpath] = mtime
                    changed.append(fpath)
        except FileNotFoundError:
            pass
        return changed

    def poll(self):
        changed = self._scan()
        for fpath in changed:
            pass  # BUG 2: should call each callback with fpath
        return len(changed)
