# Mission 086 - Backup Catalogue Fields
# Reports on the nightly backup catalogue using named fields.
from collections import namedtuple

Backup = namedtuple("Backup", "name host created_day size_gb ok")


def total_size_gb(backups):
    return sum(b[2] for b in backups)


def failed_hosts(backups):
    return sorted({b.host for b in backups if not b.ok})


def oldest(backups):
    if not backups:
        return None
    return min(backups, key=lambda b: b.created_day).name


def stale(backups, today):
    return sorted(b.name for b in backups if today - b.created > 7)


def summary(backups, today):
    return (
        f"{len(backups)} backups, {total_size_gb(backups)} GB, "
        f"{len(stale(backups, today))} stale"
    )


if __name__ == "__main__":
    data = [
        Backup("db-mon", "db1", 100, 40, True),
        Backup("db-tue", "db1", 101, 42, False),
        Backup("web-tue", "web1", 90, 5, True),
    ]
    print(summary(data, 102))
