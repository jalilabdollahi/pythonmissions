# Mission 133 - Pod Memory Math
# Parse Kubernetes memory quantities and check whether pods fit on a node.
import re

FACTORS = {
    "": 1,
    "Ki": 1024,
    "Mi": 1024**2,
    "Gi": 1024**3,
    "Ti": 1024**4,
    "K": 1024,
    "M": 1024**2,
    "G": 1024**3,
    "T": 1024**4,
}
QUANTITY_RE = re.compile(r"^(\d+(?:\.\d+)?)(Ki|Mi|Gi|Ti|K|M|G|T)?$")


def parse_memory(text):
    match = QUANTITY_RE.match(str(text).strip())
    if match is None:
        raise ValueError(f"invalid memory quantity: {text!r}")
    number, suffix = match.groups()
    return int(float(number)) * FACTORS[suffix or ""]


def total_requests(pods):
    total = 0
    for pod in pods:
        for container in pod.get("containers", []):
            request = container.get("memory")
            if request:
                total += parse_memory(request)
    return total


def fits_on_node(pods, node_bytes):
    return total_requests(pods) < node_bytes
