# Mission 158 - Page Turner (solution)
# Collect every item from a token-paginated API with an optional limit.


def fetch_all(client, limit=None):
    if limit is not None and limit <= 0:
        return [], 0
    items = []
    pages = 0
    page = client(None)
    while True:
        pages += 1
        items.extend(page["items"])
        if limit is not None and len(items) >= limit:
            break
        if page["next_token"] is None:
            break
        page = client(page["next_token"])
    return (items if limit is None else items[:limit]), pages


def collect_names(client, limit=None):
    items, _ = fetch_all(client, limit)
    return [server["name"] for server in items]
