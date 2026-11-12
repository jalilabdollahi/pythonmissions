# Mission 265 - Lanternfish Trace Flamegraph (solution)
# Build a trace tree from flat spans and compute how much time each span spent on its own.


def build_tree(spans):
    """spans: dicts with id, parent, service, name, start, end (milliseconds).

    Returns root nodes. A span whose parent is not part of the trace (it was
    dropped or sampled out) is promoted to a root instead of being lost.
    """
    nodes = {s["id"]: dict(s, children=[]) for s in spans}
    roots = []
    for s in spans:
        node = nodes[s["id"]]
        parent = nodes.get(s["parent"])
        if parent is None:
            roots.append(node)
        else:
            parent["children"].append(node)
    order = lambda n: (n["start"], n["end"])
    for node in nodes.values():
        node["children"].sort(key=order)
    roots.sort(key=order)
    return roots


def covered_time(node):
    """Milliseconds of `node` during which at least one child was running."""
    lo, hi = node["start"], node["end"]
    intervals = sorted((max(c["start"], lo), min(c["end"], hi)) for c in node["children"])
    total = 0
    cur_start = cur_end = None
    for start, end in intervals:
        if end <= start:
            continue
        if cur_end is None or start > cur_end:
            if cur_end is not None:
                total += cur_end - cur_start
            cur_start, cur_end = start, end
        else:
            cur_end = max(cur_end, end)
    if cur_end is not None:
        total += cur_end - cur_start
    return total


def self_time(node):
    return (node["end"] - node["start"]) - covered_time(node)


def walk(roots):
    for root in roots:
        stack = [root]
        while stack:
            node = stack.pop()
            yield node
            stack.extend(reversed(node["children"]))


def self_times(roots):
    return {n["id"]: self_time(n) for n in walk(roots)}


def time_by_service(roots):
    totals = {}
    for node in walk(roots):
        totals[node["service"]] = totals.get(node["service"], 0) + self_time(node)
    return dict(sorted(totals.items(), key=lambda kv: (-kv[1], kv[0])))


def render(roots):
    lines = []

    def visit(node, depth):
        dur = node["end"] - node["start"]
        lines.append(f"{'  ' * depth}{node['service']}:{node['name']} {dur}ms (self {self_time(node)}ms)")
        for child in node["children"]:
            visit(child, depth + 1)

    for root in roots:
        visit(root, 0)
    return "\n".join(lines)


if __name__ == "__main__":
    demo = [
        {"id": "a", "parent": None, "service": "web", "name": "GET /cart", "start": 0, "end": 100},
        {"id": "b", "parent": "a", "service": "db", "name": "select", "start": 10, "end": 40},
    ]
    print(render(build_tree(demo)))
