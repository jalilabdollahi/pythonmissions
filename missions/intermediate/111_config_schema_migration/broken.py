# Mission 111 - Config Schema Migration
# Fix the 2 bugs in this script.

class MigrationRunner:
    def __init__(self):
        self._migrations = {}  # version -> migration_fn

    def register(self, version, fn):
        self._migrations[version] = fn

    def _version_key(self, v):
        return v  # BUG 1: string comparison is wrong for "1.10" vs "1.9" — use tuple of ints

    def run(self, config):
        """Apply all migrations in order."""
        current = config.get("version", "0.0")
        pending = sorted(
            [(v, fn) for v, fn in self._migrations.items() if v > current],  # BUG 2: string comparison
            key=lambda x: self._version_key(x[0]),
            reverse=True,  # BUG 3 (bonus): should be ascending not descending
        )
        for version, fn in pending:
            config = fn(config)
            config["version"] = version
        return config
