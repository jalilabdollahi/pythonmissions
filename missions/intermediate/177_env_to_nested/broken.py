# Mission 177 - Double Underscore
# Turn APP__SECTION__KEY environment variables into a typed nested config.
def coerce(value):
    lowered = value.strip().lower()
    if lowered in ("true", "false"):
        return bool(value)
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        return value


def env_to_nested(environ, prefix="PAY__"):
    config = {}
    for name, raw in environ.items():
        if prefix not in name:
            continue
        parts = name[len(prefix):].lower().split("__")
        node = config
        for part in parts[:-1]:
            node[part] = {}
            node = node[part]
        node[parts[-1]] = coerce(raw)
    return config


def describe_types(config, indent=0):
    lines = []
    for key in sorted(config):
        value = config[key]
        if isinstance(value, dict):
            lines.append("%s%s:" % (" " * indent, key))
            lines.extend(describe_types(value, indent + 2))
        else:
            lines.append("%s%s = %s (%s)" % (" " * indent, key, value, type(value).__name__))
    return lines
