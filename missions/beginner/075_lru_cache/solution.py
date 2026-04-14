# Mission 075 - Solution
import functools

_DB = {"host": "localhost", "port": "5432", "db": "myapp"}

@functools.lru_cache(maxsize=None)
def cached_get(key):
    print(f"  [DB hit] {key}")
    return _DB.get(key)

if __name__ == "__main__":
    print(cached_get("host"))
    print(cached_get("host"))
