# Mission 134 - Millicore Ledger (solution)
# Convert Kubernetes CPU quantities to millicores and total them per namespace.
import re

CPU_RE = re.compile(r"^(\d+(?:\.\d+)?)(m?)$")


def parse_cpu(text):
    match = CPU_RE.match(str(text).strip())
    if match is None:
        raise ValueError(f"invalid cpu quantity: {text!r}")
    number, milli = match.groups()
    if milli:
        return int(number)
    return round(float(number) * 1000)


def pod_millicores(pod):
    total = 0
    for container in pod["containers"]:
        request = container.get("cpu")
        if request:
            total += parse_cpu(request)
    return total


def namespace_totals(pods):
    totals = {}
    for pod in pods:
        ns = pod.get("namespace", "default")
        totals[ns] = totals.get(ns, 0) + pod_millicores(pod)
    return totals
