# Mission 046 - One Line of the Log
# Summarise an nginx-style error log for the morning stand-up.


def summarize_log(path):
    with open(path, encoding="utf-8") as handle:
        lines = handle.readline()
    errors = [line for line in lines if "ERROR" in line]
    return len(lines), len(errors)


def last_lines(path, count):
    with open(path, encoding="utf-8") as handle:
        lines = handle.read().splitlines()
    return lines[-count:] if count else []
