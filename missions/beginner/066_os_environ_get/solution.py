# Mission 066 - Solution
import os

def get_db_password():
    return os.environ.get("DB_PASSWORD", "changeme")

if __name__ == "__main__":
    print(get_db_password())
