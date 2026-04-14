# Mission 046 - SQL Query Builder
# Fix the 2 bugs in this script.

def build_select(table, conditions=None, limit=None):
    """Build a parameterized SELECT query."""
    query = f"SELECT * FROM {table}"  # table name is safe (internal)
    params = []
    if conditions:
        clauses = []
        for col, val in conditions.items():
            clauses.append(f"{col} = ?")
            params.append(val)
        query += " WHERE " + " ".join(clauses)  # BUG 1: should join with " AND "
    if limit:
        query += f" LIMIT {limit}"  # BUG 2: limit should be parameterized
    return query, params
