# Mission 126 - Dotenv Dialect (solution)
# Parse .env text (comments, export prefix, quotes, '=' inside values).


def unquote(value):
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def parse_line(line):
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    if line.startswith("export "):
        line = line[len("export "):].lstrip()
    if "=" not in line:
        return None
    key, value = line.split("=", 1)
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
