# Mission 290 - Backup Rotation (solution)
# Grandfather-father-son retention: pick which backups to keep and which to delete.
from datetime import datetime


def _newest_per_period(newest_first, period_of, limit):
    """Keep the newest backup of each of the `limit` most recent periods."""
    chosen = {}
    for stamp in newest_first:
        period = period_of(stamp)
        if period in chosen:
            continue
        if len(chosen) == limit:
            break
        chosen[period] = stamp
    return set(chosen.values())


def tiers_for(backups, daily=7, weekly=4, monthly=6):
    """Which backups each tier keeps: sons (daily), fathers (weekly), grandfathers (monthly)."""
    newest_first = sorted(set(backups), reverse=True)
    sons = _newest_per_period(newest_first, lambda d: d.date(), daily)
    fathers = _newest_per_period(newest_first, lambda d: d.isocalendar()[:2], weekly)
    grandfathers = _newest_per_period(newest_first, lambda d: (d.year, d.month), monthly)
    return {
        "son": sorted(sons),
        "father": sorted(fathers),
        "grandfather": sorted(grandfathers),
    }


def select_keep(backups, daily=7, weekly=4, monthly=6):
    """Return the set of backup datetimes to retain (the union of the three tiers).

    sons: newest backup of each of the last `daily` calendar days
    fathers: newest backup of each of the last `weekly` ISO weeks
    grandfathers: newest backup of each of the last `monthly` calendar months
    """
    keep = set()
    for kept in tiers_for(backups, daily, weekly, monthly).values():
        keep.update(kept)
    return keep


def plan(backups, **limits):
    keep = select_keep(backups, **limits)
    return {
        "keep": sorted(keep),
        "delete": sorted(set(backups) - keep),
    }


def parse_backup_name(name):
    """db-20240612T0230.tar.gz -> datetime(2024, 6, 12, 2, 30)."""
    stamp = name.split("-", 1)[1].split(".", 1)[0]
    return datetime.strptime(stamp, "%Y%m%dT%H%M")


def names_to_delete(names, **limits):
    by_time = {parse_backup_name(n): n for n in names}
    doomed = plan(list(by_time), **limits)["delete"]
    return [by_time[t] for t in doomed]


def is_stale(backups, now, max_age_hours=26):
    """Alert condition: there is no recent backup at all (or none whatsoever)."""
    if not backups:
        return True
    age = now - max(backups)
    return age.total_seconds() > max_age_hours * 3600


def savings(backups, **limits):
    """Fraction of stored backups the policy lets us delete."""
    unique = set(backups)
    if not unique:
        return 0.0
    return len(plan(unique, **limits)["delete"]) / len(unique)
