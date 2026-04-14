# Mission 080 - API Pagination
# Fix the 2 bugs in this script.
import math

def total_pages(total_items, per_page):
    return total_items // per_page  # BUG 1: integer division loses partial page

def fetch_all_pages(session, base_url, per_page=100):
    """Fetch all pages and return combined results."""
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
        break  # BUG 2: exits after first page unconditionally
        page += 1
    return results
