# Mission 054 - Solution
def run_query(conn, sql):
    try:
        result = conn.execute(sql)
        return result
    except Exception as e:
        raise RuntimeError(f"Query failed: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    class FakeConn:
        def execute(self, sql): raise ValueError("bad sql")
        def close(self): print("closed")
    try:
        run_query(FakeConn(), "SELECT bad")
    except RuntimeError:
        pass
