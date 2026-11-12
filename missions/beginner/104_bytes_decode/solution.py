# Mission 104 - Silent Service Check (solution)
# Interprets raw command output from a service manager.
def read_state(runner, unit):
    raw = runner(["systemctl", "is-active", unit])
    return raw.decode("utf-8").strip().lower()


def failed_units(runner, units):
    return [unit for unit in units if read_state(runner, unit) != "active"]


def active_units(raw):
    text = raw.decode("utf-8")
    names = []
    for line in text.split("\n"):
        fields = line.split()
        if len(fields) >= 3 and fields[2] == "active":
            names.append(fields[0])
    return names


def summary(runner, units):
    bad = failed_units(runner, units)
    if not bad:
        return "all units active"
    return "failed: " + ", ".join(bad)


if __name__ == "__main__":
    import subprocess

    def real_runner(argv):
        return subprocess.run(argv, capture_output=True).stdout

    print(summary(real_runner, ["ssh.service"]))
