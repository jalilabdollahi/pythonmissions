# Mission 005 - The Flag That Never Turns Off (solution)
# Parses boolean feature flags from environment variables.
TRUE_VALUES = {"1", "true", "yes", "on"}


def flag_enabled(env, name):
    return env.get(name, "").strip().lower() in TRUE_VALUES


def enabled_flags(env, names):
    return [name for name in names if flag_enabled(env, name)]


if __name__ == "__main__":
    import os

    print(enabled_flags(os.environ, ["DEBUG", "TRACE_PAYLOADS", "DRY_RUN"]))
