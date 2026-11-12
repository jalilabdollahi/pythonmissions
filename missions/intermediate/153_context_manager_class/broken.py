# Mission 153 - Deploy Lock Guard
# A lock-file context manager that serialises production deploys.
import os


class LockHeld(Exception):
    pass


class DeployLock:
    def __init__(self, path, owner):
        self.path = str(path)
        self.owner = owner
        self.held = False

    def __enter__(self):
        try:
            with open(self.path, "x") as handle:
                handle.write(self.owner)
        except FileExistsError:
            raise LockHeld(f"deploy lock {self.path} is already held") from None
        self.held = True

    def __exit__(self, exc_type, exc, tb):
        if exc_type is None:
            self.release()
        return True

    def release(self):
        if self.held:
            os.remove(self.path)
            self.held = False


def current_owner(path):
    try:
        with open(path) as handle:
            return handle.read()
    except FileNotFoundError:
        return None
