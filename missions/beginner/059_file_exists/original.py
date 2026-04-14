# Mission 059 - Check Before Reading
import os

def file_exists(path):
    """Return True if path exists on the filesystem."""
    return os.path.exist(path)

if __name__ == "__main__":
    print(file_exists("/etc/hosts"))
    print(file_exists("/nonexistent"))
