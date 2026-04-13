# Mission 15 - Webhook Alert
# Fix the 2 bugs in this script.

import json
from datetime import datetime

import requests


def send_alert(webhook_url, title, message, severity="warning"):
    COLOR = {"info": "#36a64f", "warning": "#ff9900", "critical": "#cc0000"}

    payload = {
        "text": f"*{title}*",
        "attachments": [
            {
                "color": COLOR.get(severity, "#cccccc"),
                "text": message,
                "footer": f"PythonMissions Alert - {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}",
            }
        ],
    }

    response = requests.post(
        webhook_url,
        data=payload,
        timeout=10,
    )
    response.raise_for_status()
    return response.status_code


def send_deploy_alert(webhook_url, service, version, environment, deployer):
    title = f"Deployed: {service} v{version}"
    message = f"*Environment:* {environment}\n*Deployed by:* {deployer}"
    return send_alert(webhook_url, title, message, severity="info")


def send_incident_alert(webhook_url, service, error_message):
    title = f"INCIDENT: {service} is down"
    message = f"*Error:* {error_message}\n*Time:* {datetime.utcnow().isoformat()}"
    return send_alert(webhook_url, title, message, severity="critical")


if __name__ == "__main__":
    import sys
    webhook = sys.argv[1] if len(sys.argv) > 1 else "https://hooks.slack.com/YOUR_WEBHOOK"
    send_deploy_alert(webhook, "api-gateway", "3.1.4", "production", "jalil")
    print("Alert sent!")
