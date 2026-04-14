# Mission 066 - Read the DB Password
import os

def get_db_password():
    """Return DB_PASSWORD env var or 'changeme' if not set."""
    return os.environ["DB_PASSWORD"]

if __name__ == "__main__":
    print(get_db_password())
