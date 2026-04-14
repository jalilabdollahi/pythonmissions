# Mission 090 - Solution
def process_lines(lines):
    return [stripped for line in lines if (stripped := line.strip())]

if __name__ == "__main__":
    raw = ["  ERROR: disk full  ", "", "  WARN: high cpu  ", "  "]
    print(process_lines(raw))
