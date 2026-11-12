# Mission 005 - The Flag That Never Turns Off
# Parses boolean feature flags from environment variables.
TRUE_VALUES = {"1", "true", "yes", "on"}


def flag_enabled(env, name):
    return bool(env.get(name, ""))


def enabled_flags(env, names):
    return [name for name in names if flag_enabled(env, name)]


if __name__ == "__main__":
    import os

    print(enabled_flags(os.environ, ["DEBUG", "TRACE_PAYLOADS", "DRY_RUN"]))
