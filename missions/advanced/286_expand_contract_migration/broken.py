# Mission 286 - Rename Without Downtime
# Linter that checks a column rename is split into safe expand, migrate and contract steps.


def add_column(table, column, **options):
    return {"op": "add_column", "table": table, "column": column, **options}


def dual_write(table, column):
    return {"op": "dual_write", "table": table, "column": column}


def backfill(table, column):
    return {"op": "backfill", "table": table, "column": column}


def switch_reads(table, column):
    return {"op": "switch_reads", "table": table, "column": column}


def drop_column(table, column, replaced_by):
    return {"op": "drop_column", "table": table, "column": column, "replaced_by": replaced_by}


def validate_plan(steps):
    """Return a list of (step_index, message) problems; an empty list means the plan is safe."""
    errors = []
    state = {}

    def column_state(table, column):
        return state.setdefault(
            column,
            {"added": False, "dual": False, "backfilled": False, "switched": False},
        )

    for index, step in enumerate(steps):
        op, table, column = step["op"], step["table"], step["column"]
        current = column_state(table, column)
        if op == "add_column":
            if current["added"]:
                errors.append((index, f"{table}.{column} was already added"))
            if not step.get("nullable"):
                errors.append((index, f"{table}.{column} must be nullable or have a default"))
            current["added"] = True
        elif op == "dual_write":
            if not current["added"]:
                errors.append((index, f"{table}.{column} is dual-written before it exists"))
            current["dual"] = True
        elif op == "backfill":
            if not current["added"]:
                errors.append((index, f"backfill of {table}.{column} must follow dual writes"))
            current["backfilled"] = True
        elif op == "switch_reads":
            if not current["backfilled"]:
                errors.append((index, f"{table}.{column} is read before it is backfilled"))
            current["switched"] = True
        elif op == "drop_column":
            replacement = current
            if not replacement["switched"]:
                errors.append((index, f"{table}.{column} dropped before reads moved to {step['replaced_by']}"))
        else:
            errors.append((index, f"unknown operation {op!r}"))
    return errors


def render_report(steps):
    problems = validate_plan(steps)
    if not problems:
        return f"plan of {len(steps)} steps is safe"
    return "\n".join(f"step {i}: {msg}" for i, msg in problems)
