# Mission 057 - Read All Log Lines
def read_lines(path):
    """Return list of non-empty stripped lines from file."""
    with open(path) as f:
        return [line.strip() for line in f.read() if line.strip()]

if __name__ == "__main__":
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as f:
        f.write("line1\nline2\nline3\n")
        name = f.name
    print(read_lines(name))
