# Mission 123 - Five Hundred Percent (solution)
# Compute the 5xx error rate of a service and flag services above a threshold.


def is_server_error(status):
    return 500 <= status < 600


def error_rate_percent(statuses):
    if not statuses:
        return 0.0
    errors = sum(1 for s in statuses if is_server_error(s))
    total = len(statuses)
    if total == 0:
        return 0.0
    return round(errors / total * 100, 2)


def breaching_services(by_service, threshold):
    names = []
    for service, statuses in by_service.items():
        if error_rate_percent(statuses) > threshold:
            names.append(service)
    return sorted(names)
