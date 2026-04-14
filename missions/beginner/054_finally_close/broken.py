# Mission 054 - Always Close the Connection
def run_query(conn, sql):
    """Run SQL and always close the connection."""
    try:
        result = conn.execute(sql)
        conn.close()
        return result
    except Exception as e:
        raise RuntimeError(f"Query failed: {e}")

if __name__ == "__main__":
    class FakeConn:
        def execute(self, sql): raise ValueError("bad sql")
        def close(self): print("closed")
    try:
        run_query(FakeConn(), "SELECT bad")
    except RuntimeError:
        pass
