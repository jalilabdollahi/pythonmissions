# Mission 216 - Schema Migration Runner (solution)
# Apply numbered SQL migrations exactly once, in order.
import sqlite3


def ensure_table(conn):
    conn.execute("CREATE TABLE IF NOT EXISTS schema_migrations (version TEXT PRIMARY KEY)")
    conn.commit()


def applied_versions(conn):
    rows = conn.execute("SELECT version FROM schema_migrations").fetchall()
    return {row[0] for row in rows}


def pending_versions(migrations, applied):
    return [v for v in sorted(migrations, key=int) if v not in applied]


def apply_one(conn, version, sql):
    conn.execute(sql)
    conn.execute("INSERT INTO schema_migrations (version) VALUES (?)", (version,))
    conn.commit()


def migrate(conn, migrations):
    ensure_table(conn)
    done = []
    for version in pending_versions(migrations, applied_versions(conn)):
        apply_one(conn, version, migrations[version])
        done.append(version)
    return done


def current_version(conn):
    versions = [int(v) for v in applied_versions(conn)]
    return max(versions) if versions else 0


if __name__ == "__main__":
    db = sqlite3.connect(":memory:")
    print(migrate(db, {"1": "CREATE TABLE svc (name TEXT)", "2": "ALTER TABLE svc ADD COLUMN owner TEXT"}))
