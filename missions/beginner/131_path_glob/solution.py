# Mission 131 - Solution
from pathlib import Path

def find_yaml_files(directory):
    return list(Path(directory).glob("*.yaml"))

if __name__ == "__main__":
    import tempfile
    d = tempfile.mkdtemp()
    Path(d, "config.yaml").write_text("host: localhost")
    print(find_yaml_files(d))
