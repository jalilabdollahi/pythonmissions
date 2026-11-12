# Mission 164 - Rolling Logs (solution)
# Size-based log rotation with numbered backups.
import os


def needs_rotation(path, max_bytes):
    return os.path.exists(path) and os.path.getsize(path) >= max_bytes


def rotate(path, keep=3):
    path = os.fspath(path)
    for i in range(keep - 1, 0, -1):
        older = f"{path}.{i}"
        if os.path.exists(older):
            os.replace(older, f"{path}.{i + 1}")
    if os.path.exists(path):
        os.replace(path, f"{path}.1")
    with open(path, "w"):
        pass


def maybe_rotate(path, max_bytes, keep=3):
    if needs_rotation(path, max_bytes):
        rotate(path, keep)
        return True
    return False
