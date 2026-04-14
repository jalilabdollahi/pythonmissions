# Mission 027 - API Health Checker
# Fix the 2 bugs in this script.

def check_endpoint(url, session):
    """Returns True if the endpoint is healthy."""
    try:
        response = session.get(url, timeout=5)
        return response.status_code == 200  # BUG 1: should accept any 2xx (200-299)
    except Exception:
        return False  # BUG 2: should at least log or re-raise connection errors

def check_all(endpoints, session):
    results = {}
    for url in endpoints:
        results[url] = check_endpoint(url, session)
    return results
