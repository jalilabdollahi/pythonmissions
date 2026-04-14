# Mission 013 - Check the Log Extension
# Fix the bug.

def is_log_file(filename):
    """Return True if the filename has a .log extension."""
    return filename.endswith(".txt")

def filter_logs(files):
    return [f for f in files if is_log_file(f)]

if __name__ == "__main__":
    files = ["app.log", "config.yaml", "error.log", "readme.txt"]
    print(filter_logs(files))
