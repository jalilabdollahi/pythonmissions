# Mission 059 - Solution
import os

def file_exists(path):
    return os.path.exists(path)

if __name__ == "__main__":
    print(file_exists("/etc/hosts"))
    print(file_exists("/nonexistent"))
