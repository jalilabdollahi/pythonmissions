# Mission 048 - Log Rotation Handler
# Fixed solution
import os

class LogRotator:
    def __init__(self, log_path, archive_path, max_bytes=1024*1024):
        self.log_path = log_path
        self.archive_path = archive_path
        self.max_bytes = max_bytes

    def should_rotate(self):
        if not os.path.exists(self.log_path):
            return False
        size = os.path.getsize(self.log_path)
        return size > self.max_bytes

    def rotate(self):
        if not self.should_rotate():
            return False
        with open(self.log_path, "r") as src:
            content = src.read()
        with open(self.archive_path, "w") as dst:
            dst.write(content)
        with open(self.log_path, "w") as f:
            f.write("")
        return True

    def write(self, message):
        self.rotate()
        with open(self.log_path, "a") as f:
            f.write(message + "\n")
        return os.path.getsize(self.log_path) <= self.max_bytes
