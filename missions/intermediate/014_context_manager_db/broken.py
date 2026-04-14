# Mission 014 - Database Context Manager
# Fix the 2 bugs in this script.

class FakeDB:
    def __init__(self, dsn):
        self.dsn = dsn
        self.connected = False

    def connect(self):
        self.connected = True
        return self

    def disconnect(self):
        self.connected = False

    def __enter__(self):
        return self.connect()

    def __exit__(self):  # BUG 1: missing exc_type, exc_val, exc_tb
        self.disconnect()
        return True

def query_db(dsn, sql):
    db = FakeDB(dns)  # BUG 2: typo — dns should be dsn
    with db:
        return f"result of: {sql}"
