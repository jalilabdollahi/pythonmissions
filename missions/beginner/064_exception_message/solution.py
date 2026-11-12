# Mission 064 - Error Text Went Missing (solution)
# Validates port strings and builds a report of the invalid ones.


def to_port(text):
    number = int(text)
    if not 1 <= number <= 65535:
        raise ValueError("port %d is out of range" % number)
    return number


def check_port(text):
    try:
        to_port(text)
    except ValueError as error:
        return False, str(error)
    return True, ""


def failure_report(values):
    lines = []
    for value in values:
        ok, reason = check_port(value)
        if not ok:
            lines.append("%s: %s" % (value, reason))
    return lines


def all_ok(values):
    return all(check_port(value)[0] for value in values)


if __name__ == "__main__":
    for line in failure_report(["80", "abc", "70000"]):
        print(line)
