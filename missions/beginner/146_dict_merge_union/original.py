# Mission 146 - Merge Configs with Union Operator
def merge(base, override):
    """Return new dict merging base with override (non-destructive)."""
    base |= override
    return base

if __name__ == "__main__":
    b = {"host": "localhost", "port": 5432}
    o = {"port": 5433, "debug": True}
    result = merge(b, o)
    print("base:", b)
    print("result:", result)
