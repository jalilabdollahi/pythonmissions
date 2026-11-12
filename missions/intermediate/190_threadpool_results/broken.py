# Mission 190 - Pool Party Results
# Probe many hosts with a thread pool, keeping order and keeping failures.
from concurrent.futures import ThreadPoolExecutor, as_completed


def probe_all(hosts, probe, workers=4):
    results = []
    with ThreadPoolExecutor(max_workers=len(hosts) or 1) as pool:
        futures = [pool.submit(probe, host) for host in hosts]
        for future in as_completed(futures):
            host = hosts[futures.index(future)]
            try:
                results.append({"host": host, "ok": True, "value": future.result()})
            except TimeoutError as exc:
                message = "%s: %s" % (type(exc).__name__, exc)
                results.append({"host": host, "ok": False, "error": message})
    return results


def failed_hosts(results):
    return [r["host"] for r in results if not r["ok"]]


def main():
    def probe(host):
        if host.endswith("9"):
            raise OSError("unreachable")
        return "reachable"

    results = probe_all(["r1", "r2", "r9"], probe, workers=2)
    for entry in results:
        print(entry)
    print("failed:", failed_hosts(results))


if __name__ == "__main__":
    main()
