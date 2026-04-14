# Mission 090 - Parse Non-Empty Lines
def process_lines(lines):
    """Return stripped non-empty lines."""
    return [line.strip() for line in lines if line.strip()]

if __name__ == "__main__":
    raw = ["  ERROR: disk full  ", "", "  WARN: high cpu  ", "  "]
    print(process_lines(raw))
