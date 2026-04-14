# Mission 036 - Pop with a Safety Net
# Fix the bug.

def remove_flag(flags, name):
    """Remove and return the flag, or False if not present."""
    return flags.pop(name)

if __name__ == "__main__":
    flags = {"dark_mode": True, "beta_api": False}
    print(remove_flag(flags, "dark_mode"))
    print(remove_flag(flags, "nonexistent"))
