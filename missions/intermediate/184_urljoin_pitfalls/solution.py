# Mission 184 - Lost In The Path (solution)
# Build API URLs from a base, a resource path and query parameters.
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit


def join_url(base, path):
    return urljoin(base.rstrip("/") + "/", path.lstrip("/"))


def with_query(url, params):
    parts = urlsplit(url)
    pairs = parse_qsl(parts.query, keep_blank_values=True)
    pairs.extend(sorted(params.items()))
    query = urlencode(pairs)
    return urlunsplit((parts.scheme, parts.netloc, parts.path, query, parts.fragment))


def endpoint(base, resource, **params):
    url = join_url(base, resource)
    return with_query(url, params) if params else url


def api_urls(base, resources):
    return [join_url(base, r) for r in resources]


def main():
    base = "https://api.tidewater.example/v2"
    print(endpoint(base, "claims/17"))
    print(endpoint(base, "/claims", status="open", q="water damage"))
    for url in api_urls(base, ["policies", "/agents"]):
        print(url)


if __name__ == "__main__":
    main()
