# Mission 034 - Alert Template Builder
# Fix the 2 bugs in this script.

ALERT_TEMPLATE = "ALERT [{severity}] {service} on {host}: {message}"

def build_alert(severity, service, host, message):
    context = {
        "severity": severity,
        "service": service,
        "hostname": host,  # BUG 1: key is "hostname" but template uses "host"
        "message": message,
    }
    return ALERT_TEMPLATE.format(context)  # BUG 2: should be format_map(context)

def format_pagerduty(alert):
    return f"PD: {alert.upper()}"
