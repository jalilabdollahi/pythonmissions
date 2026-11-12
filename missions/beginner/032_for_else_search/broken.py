# Mission 032 - No Free Port Found
# Pick a free TCP port for a preview environment from a reserved range.


def first_free_port(start, end, in_use):
    taken = set(in_use)
    for port in range(start, end):
        if port in taken:
            break
    else:
        raise RuntimeError(f"no free port between {start} and {end}")
    return port


def allocate(start, end, in_use):
    port = first_free_port(start, end, in_use)
    return port, set(in_use) | {port}
