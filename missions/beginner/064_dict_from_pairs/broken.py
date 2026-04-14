# Mission 064 - Build Dict from Key=Value Lines
def parse_kv_lines(lines):
    """Parse 'key=value' lines into a dict."""
    return [tuple(line.split("=", 1)) for line in lines if "=" in line]

if __name__ == "__main__":
    lines = ["host=localhost", "port=5432", "db=myapp"]
    print(parse_kv_lines(lines))
