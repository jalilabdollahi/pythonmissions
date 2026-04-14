# Mission 075 - Cache the Config Lookup
import functools

_DB = {"host": "localhost", "port": "5432", "db": "myapp"}

@functools.cache
def cached_get(key):
    """Return config value for key (cached)."""
    print(f"  [DB hit] {key}")
    return _DB.get(key)

if __name__ == "__main__":
    print(cached_get("host"))
    print(cached_get("host"))
