# Mission 031 - Comments Cut the Config (solution)
# Parse a KEY=VALUE feature-flag file that contains comments.


def load_flags(text):
    flags = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("#"):
            continue
        key, _, value = line.partition("=")
        flags[key.strip()] = value.strip()
    return flags


def enabled_flags(flags):
    return sorted(name for name, value in flags.items() if value == "on")
