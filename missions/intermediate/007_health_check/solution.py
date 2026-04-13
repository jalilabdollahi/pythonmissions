# Mission 07 - Solution

import requests


def check_endpoint(url):
    try:
        response = requests.get(url, timeout=5)

        status_code = response.status_code
        healthy = status_code == 200

        return {
            "url": url,
            "status_code": status_code,
            "healthy": healthy,
            "error": None,
        }
    except requests.exceptions.RequestException as e:
        return {
            "url": url,
            "status_code": None,
            "healthy": False,
            "error": str(e),
        }


def check_all(urls):
    results = [check_endpoint(url) for url in urls]
    healthy_count = sum(1 for r in results if r["healthy"])
    return {
        "results": results,
        "total": len(urls),
        "healthy": healthy_count,
        "unhealthy": len(urls) - healthy_count,
    }


if __name__ == "__main__":
    urls = ["http://localhost:8080/health", "http://localhost:9090/health"]
    summary = check_all(urls)
    print(f"Healthy: {summary['healthy']}/{summary['total']}")
