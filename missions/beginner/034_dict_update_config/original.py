# Mission 034 - Update the Config
# Fix the bug.

def merge_config(base, override):
    """Merge override values into base and return base."""
    result = dict(base)
    override.update(result)
    return result

if __name__ == "__main__":
    base = {"host": "localhost", "port": 5432, "timeout": 30}
    override = {"port": 5433, "debug": True}
    print(merge_config(base, override))
