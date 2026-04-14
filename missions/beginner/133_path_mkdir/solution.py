# Mission 133 - Solution
from pathlib import Path

def ensure_log_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    import tempfile, os
    base = tempfile.mkdtemp()
    deep_path = os.path.join(base, "a", "b", "c", "logs")
    ensure_log_dir(deep_path)
    print(os.path.exists(deep_path))
