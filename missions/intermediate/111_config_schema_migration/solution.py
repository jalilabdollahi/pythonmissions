# Mission 111 - Config Schema Migration
# Fixed solution

class MigrationRunner:
    def __init__(self):
        self._migrations = {}

    def register(self, version, fn):
        self._migrations[version] = fn

    def _version_key(self, v):
        return tuple(map(int, v.split(".")))

    def run(self, config):
        current_key = self._version_key(config.get("version", "0.0"))
        pending = sorted(
            [(v, fn) for v, fn in self._migrations.items()
             if self._version_key(v) > current_key],
            key=lambda x: self._version_key(x[0]),
        )
        for version, fn in pending:
            config = fn(config)
            config["version"] = version
        return config
