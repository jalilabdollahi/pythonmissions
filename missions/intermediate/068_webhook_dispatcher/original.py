# Mission 068 - Webhook Dispatcher
# Fix the 2 bugs in this script.
import json

def dispatch_webhook(url, event, session):
    payload = {"event": event["type"], "data": event.get("data", {})}
    response = session.post(url, data=json.dumps(payload))  # BUG 1: should use json=payload
    if response.ok == "True":  # BUG 2: response.ok is bool, not string
        return {"success": True, "status": response.status_code}
    return {"success": False, "status": response.status_code}

def dispatch_all(urls, event, session):
    return [dispatch_webhook(u, event, session) for u in urls]
