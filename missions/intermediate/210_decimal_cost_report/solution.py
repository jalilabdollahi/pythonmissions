# Mission 210 - Cloud Bill Cents (solution)
# Invoice math for re-billing cloud costs with Decimal.
from decimal import Decimal, ROUND_HALF_UP

CENT = Decimal("0.01")


def money(value):
    return value.quantize(CENT, rounding=ROUND_HALF_UP)


def line_cost(price, quantity):
    return money(Decimal(price) * quantity)


def invoice(lines):
    rows = [(name, line_cost(price, qty)) for name, price, qty in lines]
    total = sum((cost for _, cost in rows), Decimal("0.00"))
    return rows, total


def apply_discount(amount, pct):
    factor = Decimal(str(pct)) / 100
    return money(amount - amount * factor)


def team_totals(lines_by_team):
    return {team: invoice(lines)[1] for team, lines in lines_by_team.items()}


def share_of_total(rows, total):
    if not total:
        return {}
    return {name: (cost / total * 100).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP) for name, cost in rows}


def render(rows, total):
    out = [f"{name:<12}{cost:>10}" for name, cost in rows]
    out.append(f"{'TOTAL':<12}{total:>10}")
    return "\n".join(out)


if __name__ == "__main__":
    rows, total = invoice([("gp3-volume", "0.0825", 1000), ("egress", "0.09", 120)])
    print(render(rows, total))
