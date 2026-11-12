# Mission 147 - Wrong Pager Route (solution)
# Pick the receiver for an alert from an ordered list of label-matching routes.


def route_matches(labels, match):
    return all(labels.get(key) == value for key, value in match.items())


def pick_receiver(labels, routes, default):
    chosen = default
    for route in routes:
        if route_matches(labels, route["match"]):
            return route["receiver"]
    return chosen


def route_alerts(alerts, routes, default):
    grouped = {}
    for alert in alerts:
        receiver = pick_receiver(alert["labels"], routes, default)
        grouped.setdefault(receiver, []).append(alert["name"])
    return grouped
