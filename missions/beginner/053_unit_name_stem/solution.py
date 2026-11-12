# Mission 053 - Unit Names Cut Short (solution)
# Builds an inventory of systemd units from their file names.
from pathlib import PurePath


def service_name(unit):
    return PurePath(unit).stem


def unit_type(unit):
    return PurePath(unit).suffix.lstrip(".")


def inventory(units):
    rows = []
    for unit in units:
        rows.append((service_name(unit), unit_type(unit)))
    return sorted(rows)


def timers_only(units):
    return [service_name(u) for u in units if unit_type(u) == "timer"]


def describe(units):
    lines = []
    for name, kind in inventory(units):
        lines.append("%-12s %s" % (name, kind))
    return "\n".join(lines)


if __name__ == "__main__":
    print(describe(["nginx.service", "backup.timer", "docker.socket"]))
