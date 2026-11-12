# Mission 126 - Dotenv Dialect
# Parse .env text (comments, export prefix, quotes, '=' inside values).


def unquote(value):
    return value


def parse_line(line):
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    if "=" not in line:
        return None
    key, value = line.split("=")[:2]
    return key.strip(), unquote(value.strip())


def parse_env(text):
    env = {}
    for line in text.splitlines():
        parsed = parse_line(line)
        if parsed is not None:
            key, value = parsed
            env[key] = value
    return env


def load_env_file(path):
    with open(path, encoding="utf-8") as handle:
        return parse_env(handle.read())
