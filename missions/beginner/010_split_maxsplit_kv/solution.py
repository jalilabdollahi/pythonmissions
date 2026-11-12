# Mission 010 - Equals Signs In Values (solution)
# Parses KEY=value lines from a .env style file.
def parse_line(line):
    key, value = line.split("=", 1)
    return key.strip(), value.strip()


def parse_env_text(text):
    result = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        key, value = parse_line(line)
        result[key] = value
    return result


if __name__ == "__main__":
    sample = "# jobs\nQUEUE=billing\nTOKEN=abc==\n"
    print(parse_env_text(sample))
