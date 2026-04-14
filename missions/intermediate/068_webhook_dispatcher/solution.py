# Mission 068 - Webhook Dispatcher
# Fixed solution

def dispatch_webhook(url, event, session):
    payload = {"event": event["type"], "data": event.get("data", {})}
    response = session.post(url, json=payload)
    if response.ok:
        return {"success": True, "status": response.status_code}
    return {"success": False, "status": response.status_code}

def dispatch_all(urls, event, session):
    return [dispatch_webhook(u, event, session) for u in urls]
