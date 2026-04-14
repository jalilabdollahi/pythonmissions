# Mission 056 - Write the Deploy Log
def write_log(path, message):
    """Append message to the log file."""
    with open(path, "r") as f:
        f.write(message + "\n")

if __name__ == "__main__":
    import tempfile, os
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        name = tmp.name
    write_log(name, "Deploy started")
    write_log(name, "Deploy finished")
    print(open(name).read())
