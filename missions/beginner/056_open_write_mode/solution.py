# Mission 056 - Solution
def write_log(path, message):
    with open(path, "a") as f:
        f.write(message + "\n")

if __name__ == "__main__":
    import tempfile
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        name = tmp.name
    write_log(name, "Deploy started")
    print(open(name).read())
