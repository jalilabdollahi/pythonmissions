# Mission 027 - Unwatched Servers Audit (solution)
# Compare the host inventory against the monitoring roster.


def unmonitored_hosts(cmdb, monitored):
    inventory = set(cmdb)
    roster = set(monitored)
    return sorted(inventory - roster)


def stale_monitors(cmdb, monitored):
    inventory = set(cmdb)
    roster = set(monitored)
    return sorted(roster - inventory)


def coverage_report(cmdb, monitored):
    missing = unmonitored_hosts(cmdb, monitored)
    stale = stale_monitors(cmdb, monitored)
    covered = len(set(cmdb)) - len(missing)
    return {"covered": covered, "missing": missing, "stale": stale}
