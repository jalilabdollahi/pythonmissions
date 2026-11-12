# Mission 101 - Uptime Clock Display (solution)
# Formats an uptime in seconds as HH:MM:SS for the status board.
def format_duration(total_seconds):
    total_seconds = int(total_seconds)
    if total_seconds < 0:
        raise ValueError("duration cannot be negative")
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def board_line(host, total_seconds):
    return f"{host} up {format_duration(total_seconds)}"


def longest_uptime(hosts):
    # hosts maps hostname -> uptime seconds
    best = None
    for name, seconds in hosts.items():
        if best is None or seconds > best[1]:
            best = (name, seconds)
    return best


if __name__ == "__main__":
    fleet = {"edge-1": 3725, "edge-2": 59, "edge-3": 360000}
    for name, secs in sorted(fleet.items()):
        print(board_line(name, secs))
    print("longest:", longest_uptime(fleet)[0])
