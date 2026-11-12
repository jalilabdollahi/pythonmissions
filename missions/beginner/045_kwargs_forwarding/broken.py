# Mission 045 - Options Lost in the Wrapper
# Alert helpers: a core sender, a prefixing wrapper and an audit decorator.

AUDIT = []


def send_alert(channel, message, severity="info", dry_run=False):
    return {"channel": channel, "message": message, "severity": severity, "sent": not dry_run}


def prefixed_alert(channel, message, **options):
    return send_alert(channel, "[ops] " + message)


def with_audit(func):
    def wrapper(*args, **kwargs):
        AUDIT.append(func.__name__)
        return func(*args)

    return wrapper


audited_alert = with_audit(prefixed_alert)
