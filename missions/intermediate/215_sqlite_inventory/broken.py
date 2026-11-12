# Mission 215 - Rack Inventory DB
# A tiny rack inventory on top of sqlite3.
import sqlite3


class Inventory:
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS hosts (hostname TEXT PRIMARY KEY, rack TEXT NOT NULL, cpu INTEGER NOT NULL)"
        )
        self.conn.commit()

    def add_host(self, hostname, rack, cpu):
        self.conn.execute(f"INSERT INTO hosts VALUES ('{hostname}', '{rack}', {cpu})")
        self.conn.commit()

    def get_host(self, hostname):
        cur = self.conn.execute("SELECT hostname, rack, cpu FROM hosts WHERE hostname = ?", (hostname))
        return cur.fetchone()

    def move_to_rack(self, hostname, rack):
        cur = self.conn.execute("UPDATE hosts SET rack = ? WHERE hostname = ?", (rack, hostname))
        return cur.rowcount

    def cpu_by_rack(self):
        cur = self.conn.execute("SELECT rack, SUM(cpu) FROM hosts GROUP BY rack ORDER BY rack")
        return dict(cur.fetchall())

    def hosts_in_rack(self, rack):
        cur = self.conn.execute("SELECT hostname FROM hosts WHERE rack = ? ORDER BY hostname", (rack,))
        return [row[0] for row in cur.fetchall()]

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    inv = Inventory("inventory.db")
    inv.add_host("web-01", "r1", 16)
    print(inv.get_host("web-01"))
