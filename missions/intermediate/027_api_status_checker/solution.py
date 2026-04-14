# Mission 027 - API Health Checker
# Fixed solution
import logging

logger = logging.getLogger(__name__)

def check_endpoint(url, session):
    """Returns True if the endpoint is healthy."""
    try:
        response = session.get(url, timeout=5)
        return 200 <= response.status_code < 300
    except Exception as e:
        logger.error(f"Failed to check {url}: {e}")
        return False

def check_all(endpoints, session):
    results = {}
    for url in endpoints:
        results[url] = check_endpoint(url, session)
    return results
