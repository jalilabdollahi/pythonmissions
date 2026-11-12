# Mission 276 - Plugin Hot Reload Host (solution)
# A plugin host that discovers, reloads and unloads plugin modules without a restart.
import importlib
import os
import sys


class PluginHost:
    """Every plugin is a module `<name>.py` in `directory` exposing `handle(payload)`."""

    def __init__(self, directory):
        self.directory = str(directory)
        self.modules = {}
        self.handlers = {}
        self.mtimes = {}
        self.errors = {}
        self.reload_attempts = 0

    def _path(self, name):
        return os.path.join(self.directory, name + ".py")

    def discover(self):
        return sorted(
            f[:-3] for f in os.listdir(self.directory) if f.endswith(".py") and not f.startswith("_")
        )

    def _register(self, name, module):
        self.modules[name] = module
        self.handlers[name] = module.handle
        self.mtimes[name] = os.stat(self._path(name)).st_mtime_ns

    def load_new(self):
        """Import plugins that appeared since the last scan."""
        importlib.invalidate_caches()
        loaded = []
        for name in self.discover():
            if name not in self.modules:
                self._register(name, importlib.import_module(name))
                loaded.append(name)
        return loaded

    def _unload(self, name):
        sys.modules.pop(name, None)
        for table in (self.modules, self.handlers, self.mtimes, self.errors):
            table.pop(name, None)

    def refresh(self):
        """Pick up edited, removed and new plugin files. Returns the names that changed."""
        changed = []
        for name in sorted(self.modules):
            path = self._path(name)
            if not os.path.exists(path):
                self._unload(name)
                changed.append(name)
                continue
            mtime = os.stat(path).st_mtime_ns
            if mtime == self.mtimes[name]:
                continue
            self.reload_attempts += 1
            try:
                module = importlib.reload(self.modules[name])
                handler = module.handle
            except Exception as exc:
                self.errors[name] = f"{type(exc).__name__}: {exc}"
                self.mtimes[name] = mtime
                continue
            self.errors.pop(name, None)
            self.modules[name] = module
            self.handlers[name] = handler
            self.mtimes[name] = mtime
            changed.append(name)
        changed.extend(self.load_new())
        return changed

    def dispatch(self, name, payload):
        if name not in self.handlers:
            raise KeyError(f"no such plugin: {name}")
        return self.handlers[name](payload)

    def loaded(self):
        return sorted(self.handlers)


if __name__ == "__main__":
    sys.path.insert(0, "plugins")
    host = PluginHost("plugins")
    print(host.load_new())
