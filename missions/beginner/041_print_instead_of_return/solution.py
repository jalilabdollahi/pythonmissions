# Mission 041 - Printed But Never Returned (solution)
# Build metrics endpoint URLs for the health sweep.
from urllib.parse import urlencode


def build_url(host, path, params=None):
    url = f"https://{host}/{path.lstrip('/')}"
    if params:
        url += "?" + urlencode(params)
    return url


def sweep_urls(hosts, path):
    return [build_url(host, path, {"format": "json"}) for host in hosts]
