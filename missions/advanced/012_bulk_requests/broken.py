# Mission 12 - Bulk API Requests
# Fix the 2 bugs in this script.

from concurrent.futures import ThreadPoolExecutor

import requests


def check_url(url):
    try:
        response = requests.get(url, timeout=5)
        return {
            "url": url,
            "status_code": response.status_code,
            "healthy": response.status_code == 200,
            "error": None,
        }
    except requests.exceptions.RequestException as e:
        return {
            "url": url,
            "status_code": None,
            "healthy": False,
            "error": str(e),
        }


def check_urls_concurrent(urls, max_workers=10):
    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(check_url, urls)

    return results


def summarize_results(results):
    healthy = [r for r in results if r["healthy"]]
    unhealthy = [r for r in results if not r["healthy"]]
    return {
        "total": len(results),
        "healthy": len(healthy),
        "unhealthy": len(unhealthy),
        "unhealthy_urls": [r["url"] for r in unhealthy],
    }


if __name__ == "__main__":
    urls = [
        "http://httpbin.org/status/200",
        "http://httpbin.org/status/500",
        "http://httpbin.org/status/200",
    ]
    results = check_urls_concurrent(urls)
    print(summarize_results(results))
