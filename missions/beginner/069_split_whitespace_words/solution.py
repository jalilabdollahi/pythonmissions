# Mission 069 - Double Space Deploy Command (solution)
# Parses commands typed into the team chat channel.


def parse_command(line):
    words = line.split()
    if not words or words == [""]:
        raise ValueError("empty command")
    if len(words) < 2:
        raise ValueError("missing target")
    return words[0].lower(), words[1], words[2:]


def describe(line):
    verb, target, args = parse_command(line)
    extra = " with %s" % ", ".join(args) if args else ""
    return "%s -> %s%s" % (verb, target, extra)


def is_deploy(line):
    try:
        return parse_command(line)[0] == "deploy"
    except ValueError:
        return False


def targets(lines):
    found = []
    for line in lines:
        try:
            found.append(parse_command(line)[1])
        except ValueError:
            continue
    return found


if __name__ == "__main__":
    print(describe("deploy web v2"))
