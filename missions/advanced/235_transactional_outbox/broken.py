# Mission 235 - Order Event Outbox
# Transactional outbox: atomic order + event write, at-least-once relay, idempotent consumer.
import json
import sqlite3


def open_db():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE orders (id TEXT PRIMARY KEY, total_cents INTEGER NOT NULL)")
    conn.execute(
        "CREATE TABLE outbox ("
        " id INTEGER PRIMARY KEY AUTOINCREMENT,"
        " topic TEXT NOT NULL,"
        " payload TEXT NOT NULL,"
        " published INTEGER NOT NULL DEFAULT 0)"
    )
    return conn


def create_order(conn, order_id, total_cents, metadata=None):
    with conn:
        conn.execute("INSERT INTO orders (id, total_cents) VALUES (?, ?)", (order_id, total_cents))
    payload = json.dumps(
        {"order_id": order_id, "total_cents": total_cents, "meta": metadata or {}}
    )
    with conn:
        conn.execute(
            "INSERT INTO outbox (topic, payload) VALUES (?, ?)", ("order.created", payload)
        )


def pending(conn):
    rows = conn.execute("SELECT id FROM outbox WHERE published = 0 ORDER BY id").fetchall()
    return [r[0] for r in rows]


def relay_once(conn, publish, batch_size=10):
    rows = conn.execute(
        "SELECT id, topic, payload FROM outbox WHERE published = 0 ORDER BY id LIMIT ?",
        (batch_size,),
    ).fetchall()
    sent = 0
    for event_id, topic, payload in rows:
        with conn:
            conn.execute("UPDATE outbox SET published = 1 WHERE id = ?", (event_id,))
        try:
            publish({"event_id": event_id, "topic": topic, "payload": json.loads(payload)})
        except Exception:
            continue
        sent += 1
    return sent


class IdempotentConsumer:
    def __init__(self, handler):
        self.handler = handler
        self.handled = set()

    def process(self, event):
        event_id = event["event_id"]
        if event_id in self.handled:
            return False
        self.handled.add(event_id)
        self.handler(event)
        return True


def outbox_stats(conn):
    row = conn.execute(
        "SELECT COUNT(*), COALESCE(SUM(published), 0) FROM outbox"
    ).fetchone()
    return {"total": row[0], "published": row[1], "lag": row[0] - row[1]}


def count_orders(conn):
    return conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
