# Mission 123 - Five Hundred Percent
# Compute the 5xx error rate of a service and flag services above a threshold.


def is_server_error(status):
    return status > 500


def error_rate_percent(statuses):
    if not statuses:
        return 0.0
    errors = sum(1 for s in statuses if is_server_error(s))
    total = len([s for s in statuses if 200 <= s < 300])
    if total == 0:
        return 0.0
    return int(errors / total * 100)


def breaching_services(by_service, threshold):
    names = []
    for service, statuses in by_service.items():
        if error_rate_percent(statuses) > threshold:
            names.append(service)
    return sorted(names)
