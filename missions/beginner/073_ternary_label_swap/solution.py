# Mission 073 - Green Means Down (solution)
# Converts health-check streaks into UP/DOWN badges for the status board.


def badge(consecutive_failures, threshold=3):
    return "DOWN" if consecutive_failures >= threshold else "UP"


def board(streaks, threshold=3):
    return {name: badge(count, threshold) for name, count in streaks.items()}


def down_services(streaks, threshold=3):
    return sorted(name for name, state in board(streaks, threshold).items() if state == "DOWN")


def render(streaks, threshold=3):
    lines = []
    for name in sorted(streaks):
        lines.append("%s: %s" % (name, badge(streaks[name], threshold)))
    return "\n".join(lines)


def all_up(streaks, threshold=3):
    return not down_services(streaks, threshold)


if __name__ == "__main__":
    print(render({"radar": 0, "tower": 5}))
