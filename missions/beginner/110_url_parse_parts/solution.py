# Mission 110 - Endpoint Inspector (solution)
# Breaks a service URL into scheme, host and effective port.
from urllib.parse import urlsplit

DEFAULT_PORTS = {"http": 80, "https": 443, "ssh": 22}


def url_parts(url):
    parts = urlsplit(url)
    port = parts.port or DEFAULT_PORTS.get(parts.scheme)
    return {"scheme": parts.scheme, "host": parts.hostname, "port": port}


def probe_target(url):
    parts = url_parts(url)
    return f"{parts['host']}:{parts['port']}"


def is_secure(url):
    return url_parts(url)["scheme"] in ("https", "ssh")


if __name__ == "__main__":
    for endpoint in ["https://api.marlin.io/v1", "ssh://bastion:2222"]:
        print(probe_target(endpoint))
