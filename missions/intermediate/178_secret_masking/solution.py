# Mission 178 - Redact Before Shipping (solution)
# Mask passwords, tokens and API keys in log lines before they leave the host.
import re

SECRET_RE = re.compile(r"(password|passwd|token|secret|api[_-]?key)(\s*[=:]\s*)(\S+)", re.IGNORECASE)
BEARER_RE = re.compile(r"(Bearer\s+)(\S+)")


def mask_value(value):
    if len(value) <= 8:
        return "*" * len(value)
    return "*" * (len(value) - 4) + value[-4:]


def mask_line(line):
    line = SECRET_RE.sub(lambda m: m.group(1) + m.group(2) + mask_value(m.group(3)), line)
    return BEARER_RE.sub(lambda m: m.group(1) + mask_value(m.group(2)), line)


def mask_lines(lines):
    return [mask_line(line) for line in lines]


def leaked(line, secrets):
    return [s for s in secrets if s in line]


def main():
    sample = [
        "login ok user=ana token=abcdef1234567890",
        "Authorization: Bearer 0123456789abcdef0123",
    ]
    for line in mask_lines(sample):
        print(line)


if __name__ == "__main__":
    main()
