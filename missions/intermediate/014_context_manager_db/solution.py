# Mission 014 - Database Context Manager
# Fixed solution

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

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
        return False

def query_db(dsn, sql):
    db = FakeDB(dsn)
    with db:
        return f"result of: {sql}"
