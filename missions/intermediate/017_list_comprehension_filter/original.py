# Mission 017 - Log Filter Comprehension
# Fix the 2 bugs in this script.

def filter_errors(lines):
    # Keep only lines that contain ERROR
    return [line for line in lines if "ERROR" not in line]  # BUG 1: logic inverted

def extract_ips(lines):
    # Each line starts with: IP - - [timestamp]...
    return [line.split()[1] for line in lines if line.strip()]  # BUG 2: index 0, not 1

def summarize(lines):
    errors = filter_errors(lines)
    ips = extract_ips(errors)
    return {"error_count": len(errors), "unique_ips": list(set(ips))}
