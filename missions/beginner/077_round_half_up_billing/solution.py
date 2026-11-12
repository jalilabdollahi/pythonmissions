# Mission 077 - Pennies in the Invoice (solution)
# Prices metered cloud usage with contract-correct rounding.
from decimal import Decimal, ROUND_HALF_UP

CENT = Decimal("0.01")


def line_total(units, unit_price):
    exact = Decimal(str(units)) * Decimal(str(unit_price))
    return exact.quantize(CENT, rounding=ROUND_HALF_UP)


def invoice_total(lines):
    total = Decimal("0.00")
    for units, price in lines:
        total += line_total(units, price)
    return total


def format_money(amount):
    return f"${amount:.2f}"


def describe_lines(lines):
    out = []
    for units, price in lines:
        out.append(f"{units} x {price} = {format_money(line_total(units, price))}")
    return out


if __name__ == "__main__":
    usage = [(10, "0.0125"), (3, "0.5"), (250, "0.0005")]
    for row in describe_lines(usage):
        print(row)
    print("TOTAL", format_money(invoice_total(usage)))
