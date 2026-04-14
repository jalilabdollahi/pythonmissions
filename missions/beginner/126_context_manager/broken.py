# Mission 126 - Open the Config Safely
class ConfigWriter:
    def __init__(self, path):
        self.path = path
        self.f = None

    def __enter__(self):
        self.f = open(self.path, "w")
        return self.f

    def __exit_ctx__(self, exc_type, exc_val, exc_tb):
        if self.f:
            self.f.close()
        return False

if __name__ == "__main__":
    import tempfile
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        name = tmp.name
    with ConfigWriter(name) as f:
        f.write("host=localhost\n")
    print(open(name).read())
