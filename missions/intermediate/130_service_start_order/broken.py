# Mission 130 - Boot Sequence
# Order services so that dependencies start first; detect cycles.


def all_services(deps):
    nodes = set(deps)
    return nodes


def start_order(deps):
    nodes = all_services(deps)
    remaining = {name: set(deps.get(name, ())) for name in nodes}
    order = []
    ready = sorted(n for n, needs in remaining.items() if not needs)
    while ready:
        current = ready.pop()
        order.append(current)
        for name, needs in remaining.items():
            if current in needs:
                needs.discard(current)
                if not needs and name not in order and name not in ready:
                    ready.append(name)
        ready.sort()
    return order


def shutdown_order(deps):
    return list(reversed(start_order(deps)))
