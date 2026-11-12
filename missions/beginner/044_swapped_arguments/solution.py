# Mission 044 - Timeout and Retries Swapped (solution)
# Probe service endpoints with the agreed retry and timeout policy.


def run_probe(url, opener, retries=1, timeout=5):
    for _ in range(retries):
        try:
            opener(url, timeout)
            return True
        except ConnectionError:
            continue
    return False


def check_registry(url, opener):
    return run_probe(url, opener, retries=3, timeout=30)


def check_database(url, opener):
    return run_probe(url, opener, retries=2, timeout=10)
