# Mission 131 - Find All YAML Configs
from pathlib import Path

def find_yaml_files(directory):
    """Return list of .yaml files in directory."""
    return list(Path(directory).glob("*.yml"))

if __name__ == "__main__":
    import tempfile, os
    d = tempfile.mkdtemp()
    Path(d, "config.yaml").write_text("host: localhost")
    Path(d, "deploy.yaml").write_text("env: prod")
    print(find_yaml_files(d))
