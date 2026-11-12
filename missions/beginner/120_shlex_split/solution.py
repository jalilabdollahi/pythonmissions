# Mission 120 - Command Line Splitter (solution)
# Splits recorded shell command lines into argument lists for replay.
import shlex


def parse_command(line):
    return shlex.split(line)


def flag_value(line, flag):
    words = parse_command(line)
    if flag not in words:
        return None
    position = words.index(flag)
    if position + 1 >= len(words):
        return None
    return words[position + 1]


def program_name(line):
    words = parse_command(line)
    return words[0] if words else ""


def describe(line):
    words = parse_command(line)
    return f"{program_name(line)} with {len(words) - 1} arguments"


if __name__ == "__main__":
    recorded = 'git commit -m "fix login bug" --no-verify'
    print(parse_command(recorded))
