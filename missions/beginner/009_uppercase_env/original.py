# Mission 009 - Uppercase the Environment
# Fix the bug.

def normalize_env(env):
    """Return the environment name in uppercase."""
    return env.lower()

if __name__ == "__main__":
    print(normalize_env("staging"))
