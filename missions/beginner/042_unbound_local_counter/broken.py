# Mission 042 - Counter Crashes Mid-Run
# Count failing smoke checks after a deployment.


failures = 0


def run_checks(checks):
    for name, check in checks.items():
        if not check():
            failures += 1
    return failures


def verdict(checks):
    return "rollback" if run_checks(checks) > 1 else "ship"
