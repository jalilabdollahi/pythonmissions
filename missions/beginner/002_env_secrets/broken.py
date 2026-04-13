# Mission 02 - Env Secrets
# Fix the 2 bugs in this script.

import os


def get_db_config():
    host = os.env.get("DB_HOST", "localhost")
    port = os.environ.get("DB_PORT", "5432")
    name = os.environ.get("DB_NAME", "appdb")
    return {
        "host": host,
        "port": port,
        "name": name,
    }


def connection_string():
    cfg = get_db_config()
    return f"postgresql://{cfg['host']}:{cfg['port']}/{cfg['name']}"


if __name__ == "__main__":
    cfg = get_db_config()
    print(f"Connecting to: {connection_string()}")
    print(f"Config: {cfg}")
