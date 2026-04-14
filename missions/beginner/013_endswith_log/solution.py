# Mission 013 - Solution

def is_log_file(filename):
    return filename.endswith(".log")

def filter_logs(files):
    return [f for f in files if is_log_file(f)]

if __name__ == "__main__":
    files = ["app.log", "config.yaml", "error.log", "readme.txt"]
    print(filter_logs(files))
