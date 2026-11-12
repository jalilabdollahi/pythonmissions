# Mission 242 - Report Query Builder (solution)
# Builds parameterized SELECT statements for a self-service reporting API.

SCHEMA = {
    "invoices": {"id", "customer", "status", "amount", "created_at", "note"},
    "customers": {"id", "name", "region", "tier"},
}

COMPARISONS = {
    "eq": "=",
    "ne": "!=",
    "gt": ">",
    "gte": ">=",
    "lt": "<",
    "lte": "<=",
}
DIRECTIONS = {"asc": "ASC", "desc": "DESC"}
DEFAULT_LIMIT = 100
MAX_LIMIT = 500


def _column(table, name):
    if not isinstance(name, str) or name not in SCHEMA[table]:
        raise ValueError(f"unknown column {name!r} for table {table!r}")
    return name


def _escape_like(text):
    return text.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


def _condition(table, column, op, value, params):
    column = _column(table, column)
    if op in COMPARISONS:
        if value is None and op in ("eq", "ne"):
            return f"{column} IS NULL" if op == "eq" else f"{column} IS NOT NULL"
        params.append(value)
        return f"{column} {COMPARISONS[op]} ?"
    if op == "in":
        values = list(value)
        if not values:
            return "1 = 0"
        params.extend(values)
        return f"{column} IN ({', '.join('?' for _ in values)})"
    if op in ("contains", "prefix"):
        pattern = _escape_like(str(value))
        params.append(f"%{pattern}%" if op == "contains" else f"{pattern}%")
        return f"{column} LIKE ? ESCAPE '\\'"
    raise ValueError(f"unsupported operator {op!r}")


def _limit(limit):
    if limit is None:
        return DEFAULT_LIMIT
    if isinstance(limit, bool) or not isinstance(limit, int) or limit < 1:
        raise ValueError(f"limit must be a positive integer, got {limit!r}")
    return min(limit, MAX_LIMIT)


def build_select(table, columns, where=(), order_by=(), limit=None):
    if table not in SCHEMA:
        raise ValueError(f"unknown table {table!r}")
    if not columns:
        raise ValueError("at least one column is required")
    selected = [_column(table, c) for c in columns]
    params = []
    sql = f"SELECT {', '.join(selected)} FROM {table}"
    clauses = [_condition(table, c, op, v, params) for c, op, v in where]
    if clauses:
        sql += " WHERE " + " AND ".join(clauses)
    if order_by:
        parts = []
        for column, direction in order_by:
            direction = DIRECTIONS.get(str(direction).lower())
            if direction is None:
                raise ValueError("direction must be asc or desc")
            parts.append(f"{_column(table, column)} {direction}")
        sql += " ORDER BY " + ", ".join(parts)
    sql += f" LIMIT {_limit(limit)}"
    return sql, params


def run_report(conn, table, columns, **options):
    sql, params = build_select(table, columns, **options)
    return conn.execute(sql, params).fetchall()


if __name__ == "__main__":
    print(build_select("invoices", ["id", "amount"], where=[("status", "eq", "open")]))
