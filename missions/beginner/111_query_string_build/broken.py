# Mission 111 - Search Link Builder
# Builds report URLs with query strings for the dashboard links.
BASE_PATHS = {"logs": "https://status.orchard.example/logs"}


def build_query(params):
    return "&".join(f"{key}={value}" for key, value in params.items())


def search_url(base, params):
    return base + "?" + build_query(params)


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
