# Mission 034 - Alert Template Builder
# Fixed solution

ALERT_TEMPLATE = "ALERT [{severity}] {service} on {host}: {message}"

def build_alert(severity, service, host, message):
    context = {
        "severity": severity,
        "service": service,
        "host": host,
        "message": message,
    }
    return ALERT_TEMPLATE.format_map(context)

def format_pagerduty(alert):
    return f"PD: {alert.upper()}"
