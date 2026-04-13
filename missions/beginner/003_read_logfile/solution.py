# Mission 03 - Solution


def count_errors(filepath):
    count = 0
    with open(filepath, "r") as f:
        for line in f:
            if "ERROR" in line:
                count += 1
    return count


def last_lines(filepath, n=10):
    with open(filepath, "r") as f:
        lines = f.readlines()
    return lines[-n:]


def summarize(filepath):
    errors = count_errors(filepath)
    tail = last_lines(filepath, 5)
    return {
        "error_count": errors,
        "last_5_lines": [line.rstrip() for line in tail],
    }


if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "/var/log/app.log"
    result = summarize(path)
    print(f"Errors found: {result['error_count']}")
    print("Last 5 lines:")
    for line in result["last_5_lines"]:
        print(f"  {line}")
