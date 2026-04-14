# Mission 017 (Advanced) - Plugin Hot-Swap
# Fixed solution

class PluginManager:
    def __init__(self):
        self._plugins = {}
        self._history = []

    def register(self, name, plugin):
        if name in self._plugins:
            old_plugin = self._plugins[name]
            self._history.append((name, old_plugin))
            old_plugin.teardown()
        self._plugins[name] = plugin
        plugin.setup()

    def get(self, name):
        return self._plugins.get(name)

    def hot_swap(self, name, new_plugin):
        self.register(name, new_plugin)

    def rollback(self, name):
        for hist_name, hist_plugin in reversed(self._history):
            if hist_name == name:
                self._plugins[name] = hist_plugin
                return True
        return False

class BasePlugin:
    def __init__(self, name):
        self.name = name
        self.setup_called = False
        self.teardown_called = False
    def setup(self): self.setup_called = True
    def teardown(self): self.teardown_called = True
    def execute(self, data): return data
