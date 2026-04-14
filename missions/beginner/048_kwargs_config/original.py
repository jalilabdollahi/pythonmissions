# Mission 048 - Build Config from Kwargs
# Fix the bug.

def build_config(**kwargs):
    """Return a config dict from keyword arguments."""
    return {}

if __name__ == "__main__":
    cfg = build_config(host="localhost", port=5432, debug=True)
    print(cfg)
