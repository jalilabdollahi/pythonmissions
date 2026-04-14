# Mission 008 - Join the Log Parts
# Fix the bug.

def build_message(parts):
    """Join log parts with ' | ' separator."""
    return parts.join(" | ")

if __name__ == "__main__":
    print(build_message(["ERROR", "web-01", "disk full"]))
