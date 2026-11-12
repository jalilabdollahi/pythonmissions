# Mission 017 - Crooked Status Table
# Renders a fixed-width service status table.
NAME_WIDTH = 12
STATE_WIDTH = 8
HOURS_WIDTH = 6


def render_row(name, status, uptime):
    return name.rjust(NAME_WIDTH) + " " + status.ljust(STATE_WIDTH) + " " + str(uptime).ljust(HOURS_WIDTH)


def render_table(rows):
    lines = [render_row("SERVICE", "STATE", "HOURS")]
    for name, status, uptime in rows:
        lines.append(render_row(name, status, uptime))
    return lines


if __name__ == "__main__":
    for line in render_table([("planner", "up", 340), ("lidar-feed", "down", 2)]):
        print(line)
