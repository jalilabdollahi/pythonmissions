# Mission 209 - Probe Factory
# Build per-host check functions and threshold rules from closures.


def build_checks(hosts, probe):
    checks = {}
    for host in hosts:
        checks[host] = lambda: probe(host)
    return checks


def build_threshold_rules(limits):
    rules = {}
    for name, limit in limits.items():
        rules[name] = lambda value: value > limit
    return rules


def make_counter():
    count = 0

    def tick():
        count += 1
        return count

    return tick


def run_all(checks):
    return {name: check() for name, check in checks.items()}


def summarize(results):
    ok = sum(1 for value in results.values() if value)
    return f"{ok}/{len(results)} checks passed"


def failing_rules(rules, readings):
    return sorted(name for name, value in readings.items() if rules[name](value))


if __name__ == "__main__":
    checks = build_checks(["web-1", "web-2"], lambda host: f"{host} ok")
    print(run_all(checks))
