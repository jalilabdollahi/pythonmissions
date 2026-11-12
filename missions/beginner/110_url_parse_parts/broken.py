# Mission 110 - Endpoint Inspector
# Breaks a service URL into scheme, host and effective port.
DEFAULT_PORTS = {"http": 80, "https": 443, "ssh": 22}


def url_parts(url):
    scheme, rest = url.split("://")
    netloc = rest.split("/")[0]
    if ":" in netloc:
        host, port_text = netloc.split(":")
        port = int(port_text)
    else:
        host = netloc
        port = None
    return {"scheme": scheme, "host": host, "port": port}


def probe_target(url):
    parts = url_parts(url)
    return f"{parts['host']}:{parts['port']}"


def is_secure(url):
    return url_parts(url)["scheme"] in ("https", "ssh")


if __name__ == "__main__":
    for endpoint in ["https://api.marlin.io/v1", "ssh://bastion:2222"]:
        print(probe_target(endpoint))
