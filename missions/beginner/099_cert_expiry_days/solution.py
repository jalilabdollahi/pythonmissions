# Mission 099 - Days Until the Cert Dies (solution)
# Computes certificate expiry windows from fixed timestamps.


def days_left(expires, now):
    return (expires - now).days


def hours_left(expires, now):
    return (expires - now).total_seconds() / 3600


def expiring_soon(certs, now, warn_days):
    return sorted(name for name, exp in certs.items() if days_left(exp, now) <= warn_days)


def report(certs, now, warn_days):
    lines = []
    for name in expiring_soon(certs, now, warn_days):
        lines.append(f"{name}: {days_left(certs[name], now)} days")
    return lines


def most_urgent(certs, now):
    if not certs:
        return None
    return min(certs, key=lambda n: certs[n])


if __name__ == "__main__":
    from datetime import datetime, timedelta

    fixed_now = datetime(2025, 1, 1, 12, 0, 0)
    inventory = {"shop.example.com": fixed_now + timedelta(days=12, hours=3)}
    print(report(inventory, fixed_now, 30))
