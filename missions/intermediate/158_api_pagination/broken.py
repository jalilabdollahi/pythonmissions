# Mission 158 - Page Turner
# Collect every item from a token-paginated API with an optional limit.


def fetch_all(client, limit=None):
    items = []
    pages = 0
    page = client(None)
    while page["next_token"] is not None:
        pages += 1
        items.extend(page["items"])
        if limit is not None and len(items) >= limit:
            break
        page = client(page["next_token"])
    return items, pages


def collect_names(client, limit=None):
    items, _ = fetch_all(client, limit)
    return [server["name"] for server in items]
