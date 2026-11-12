# Mission 111 - Search Link Builder (solution)
# Builds report URLs with query strings for the dashboard links.
from urllib.parse import urlencode

BASE_PATHS = {"logs": "https://status.orchard.example/logs"}


def build_query(params):
    return urlencode(params)


def search_url(base, params):
    query = build_query(params)
    return base + "?" + query if query else base


def logs_link(service, text=None):
    params = {"service": service}
    if text:
        params["q"] = text
    return search_url(BASE_PATHS["logs"], params)


def logs_home():
    return search_url(BASE_PATHS["logs"], {})


if __name__ == "__main__":
    print(logs_link("api gateway", "disk full & slow"))
    print(logs_home())
