# Mission 046 - SQL Query Builder
# Fixed solution

def build_select(table, conditions=None, limit=None):
    """Build a parameterized SELECT query."""
    query = f"SELECT * FROM {table}"
    params = []
    if conditions:
        clauses = []
        for col, val in conditions.items():
            clauses.append(f"{col} = ?")
            params.append(val)
        query += " WHERE " + " AND ".join(clauses)
    if limit:
        query += " LIMIT ?"
        params.append(limit)
    return query, params
