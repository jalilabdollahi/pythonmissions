# Mission 041 - Printed But Never Returned
# Build metrics endpoint URLs for the health sweep.
from urllib.parse import urlencode


def build_url(host, path, params=None):
    url = f"https://{host}/{path}"
    if params:
        url += "?" + urlencode(params)
    print(url)


def sweep_urls(hosts, path):
    return [build_url(host, path, {"format": "json"}) for host in hosts]
