# Mission 057 - Solution
def read_lines(path):
    with open(path) as f:
        return [line.strip() for line in f.readlines() if line.strip()]

if __name__ == "__main__":
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as f:
        f.write("line1\nline2\nline3\n")
        name = f.name
    print(read_lines(name))
