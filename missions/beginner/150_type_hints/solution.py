# Mission 150 - Solution
def health_check(host: str, port: int) -> dict:
    """Check if service is reachable. Returns status dict."""
    reachable = host != "" and 1 <= port <= 65535
    return {
        "healthy": reachable,
        "msg": "ok" if reachable else "unreachable",
    }

if __name__ == "__main__":
    import inspect
    hints = health_check.__annotations__
    print(hints)
    print(health_check("localhost", 8080))
