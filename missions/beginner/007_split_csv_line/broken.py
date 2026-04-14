# Mission 007 - Split the Config Line
# Fix the bug.

def parse_field(line, index):
    """Return the field at position index from a comma-separated line."""
    parts = line.split()
    return parts[index].strip()

if __name__ == "__main__":
    line = "prod,web-01,8080,us-east-1"
    print(parse_field(line, 2))
