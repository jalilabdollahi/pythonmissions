# Mission 068 - Truthy Minus One
# Scans log lines to decide whether to page the on-call engineer.


def has_error(line):
    return bool(line.find("ERROR"))


def error_lines(lines):
    return [line for line in lines if has_error(line)]


def first_error_index(lines):
    for number, line in enumerate(lines):
        if has_error(line):
            return number
    return -1


def should_page(lines):
    return len(error_lines(lines)) > 0


def count_levels(lines):
    counts = {"ERROR": 0, "WARN": 0, "INFO": 0}
    for line in lines:
        for level in counts:
            if line.startswith(level):
                counts[level] += 1
    return counts


if __name__ == "__main__":
    print(should_page(["INFO start", "ERROR boom"]))
