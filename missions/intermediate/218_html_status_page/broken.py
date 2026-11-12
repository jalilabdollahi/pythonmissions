# Mission 218 - Status Page Escape
# Generate a public status page from hand-edited service entries.
import html

LABELS = {"up": "Operational", "degraded": "Degraded", "down": "Down"}


def render_row(service):
    name = service["name"]
    status = service["status"] if service["status"] in LABELS else "unknown"
    label = LABELS.get(status, "Unknown")
    detail = html.escape(service.get("detail", ""), quote=False)
    return f'<tr class="{status}"><td>{name}</td><td title="{detail}">{label}</td></tr>'


def overall(services):
    statuses = {service["status"] for service in services}
    if "degraded" in statuses:
        return "Partial outage"
    if "down" in statuses:
        return "Major outage"
    return "All systems operational"


def count_by_status(services):
    counts = {}
    for service in services:
        key = service["status"] if service["status"] in LABELS else "unknown"
        counts[key] = counts.get(key, 0) + 1
    return counts


def render_page(title, services):
    rows = "\n".join(render_row(service) for service in services)
    return (
        "<!doctype html>\n"
        f"<html><head><title>{html.escape(title)}</title></head><body>\n"
        f"<h1>{html.escape(title)}</h1>\n"
        f"<p class=\"banner\">{overall(services)}</p>\n"
        f"<table>\n{rows}\n</table>\n"
        "</body></html>\n"
    )


if __name__ == "__main__":
    print(render_page("Status", [{"name": "API", "status": "up"}]))
