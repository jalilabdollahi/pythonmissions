# Mission 013 (Advanced) - Query Optimizer
# Fix the 2 bugs in this script.

class QueryOptimizer:
    def __init__(self, stats):
        self.stats = stats  # {table: row_count}

    def push_predicates(self, query):
        """Move WHERE conditions to subquery level."""
        if "joins" not in query or "where" not in query:
            return query
        pushed = {}
        remaining = []
        for predicate in query["where"]:
            table = predicate.get("table")
            if table and table in query["joins"]:
                pushed.setdefault(table, []).append(predicate)
            else:
                remaining.append(predicate)
        result = dict(query)
        result["joins"] = {
            t: {"conditions": pushed.get(t, []), **v}
            for t, v in query["joins"].items()
        }
        result["where"] = pushed  # BUG 1: should be remaining (unpushed predicates)
        return result

    def reorder_joins(self, query):
        """Sort joins smallest-first for nested loop optimization."""
        if "joins" not in query:
            return query
        joins = query["joins"]
        ordered = dict(sorted(
            joins.items(),
            key=lambda item: self.stats.get(item[0], 0),
            reverse=True,  # BUG 2: should be reverse=False (smallest first)
        ))
        return {**query, "joins": ordered}

    def optimize(self, query):
        q = self.push_predicates(query)
        return self.reorder_joins(q)
