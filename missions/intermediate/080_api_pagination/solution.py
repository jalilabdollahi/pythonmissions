# Mission 080 - API Pagination
# Fixed solution
import math

def total_pages(total_items, per_page):
    return math.ceil(total_items / per_page)

def fetch_all_pages(session, base_url, per_page=100):
    results = []
    page = 1
    while True:
        resp = session.get(f"{base_url}?page={page}&per_page={per_page}")
        data = resp.json()
        results.extend(data["items"])
        total = data["total"]
        pages = total_pages(total, per_page)
        if page >= pages:
            break
        page += 1
    return results
