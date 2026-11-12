# Mission 176 - Flatten The Tree
# Flatten nested config into dotted keys and render them as environment variables.
def flatten(data, prefix="", sep="."):
    if not isinstance(data, (dict, list)):
        return {prefix: data}
    items = data.items() if isinstance(data, dict) else []
    flat = {}
    for key, value in items:
        name = prefix + sep + str(key)
        flat.update(flatten(value, name, sep))
    return flat


def to_env_lines(flat):
    lines = []
    for key in sorted(flat):
        env_key = key.upper().replace(".", "_")
        lines.append("%s=%s" % (env_key, flat[key]))
    return lines


def describe(flat):
    width = max((len(k) for k in flat), default=0)
    return ["%s  %r" % (k.ljust(width), flat[k]) for k in sorted(flat)]


def main():
    config = {"service": {"port": 9100}, "upstreams": ["a", "b"], "labels": {}}
    flat = flatten(config)
    for line in describe(flat):
        print(line)
    print("\n".join(to_env_lines(flat)))


if __name__ == "__main__":
    main()
