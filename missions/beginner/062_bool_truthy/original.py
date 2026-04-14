# Mission 062 - Check if Service is Enabled
def is_enabled(val):
    """Return True only if val is 'true' (case-insensitive)."""
    return bool(val)

if __name__ == "__main__":
    print(is_enabled("true"))
    print(is_enabled("false"))
    print(is_enabled(""))
