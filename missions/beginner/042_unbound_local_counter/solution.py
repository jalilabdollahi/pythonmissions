# Mission 042 - Counter Crashes Mid-Run (solution)
# Count failing smoke checks after a deployment.


def run_checks(checks):
    failures = 0
    for name, check in checks.items():
        if not check():
            failures += 1
    return failures


def verdict(checks):
    return "rollback" if run_checks(checks) > 1 else "ship"
