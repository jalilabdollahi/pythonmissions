# Mission 073 - Mock Testing
# Fixed solution
import requests

def notify_slack(webhook_url, message):
    resp = requests.post(webhook_url, json={"text": message})
    if resp.status_code != 200:
        raise RuntimeError("Slack notification failed")
    return True

def notify_team(webhook_url, messages):
    results = []
    for msg in messages:
        results.append(notify_slack(webhook_url, msg))
    return results
